import copy
import logging
import queue
import threading
import time
from collections import deque

from core.global_area import Car, ChargeResult
from core.virtual_time import time_factor

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)
class ChargingZone:
    def __init__(self, fast_num, slow_num,
                 semaphore_t: threading.Semaphore,
                 semaphore_f: threading.Semaphore,
                 report_queue: queue.Queue,
                fast_speed=30, slow_speed=7, wait_queue_length=1):
        self.waiting_cond = None
        self.vir = None
        self.fast_num = fast_num
        self.slow_num = slow_num
        self.charging_piles = []
        self.fast_speed = fast_speed
        self.slow_speed = slow_speed
        self.report_queue = report_queue
        self.not_full_t = semaphore_t
        self.not_full_f = semaphore_f
        # 初始化充电桩
        self.charging_piles = [ChargingPile("T", wait_queue_length, _) for _ in range(slow_num)]
        self.charging_piles.extend(ChargingPile("F", wait_queue_length, _) for _ in range(fast_num))

        self.worker_thread = threading.Thread(target=self.charging_worker, daemon=True)

        self.not_release_cause_stop = 0
        self.reschedule_t = None
        self.reschedule_f = None

    def start(self):
        self.worker_thread.start()

    def get_state(self):
        return [copy.deepcopy(pile.to_dict()) for pile in self.charging_piles]

    def cancel(self, user_id):
        for i, pile in enumerate(self.charging_piles):
            if not pile.open:
                continue
            with pile.lock:
                if not pile.open:
                    return {"message:状态不幸变更了，再试一次吧"}
                if pile.current_vehicle is not None:
                    if pile.current_vehicle.uid == user_id:
                        pile.current_vehicle = None
                        return {"message:取消成功"}
                if pile.waiting_queue:
                    c = None
                    for _, car in enumerate(pile.waiting_queue):
                        if car.uid == user_id:
                            c = None
                            break
                    if c is not None:
                        pile.waiting_queue.remove(c)
                        return {"message:取消成功"}


    def find_pile(self, vehicle: Car):
        """寻找最优充电桩"""
        best_score = float('inf')
        best_index = -1
        for i, pile in enumerate(self.charging_piles):
            # double check
            if not pile.open or pile.mode != vehicle.mode or len(pile.waiting_queue) == pile.queue_limit:
                continue
            with pile.lock:
                if pile.open and len(pile.waiting_queue) < pile.queue_limit:
                    score = len(pile.waiting_queue)
                    if pile.current_vehicle is None:
                        score -= 100
                    if score < best_score:
                        best_score = score
                        best_index = i
        return best_index

    def assign_vehicle(self, vehicle):
        """分配车辆到充电桩"""
        index = self.find_pile(vehicle)
        if index < 0:
            return False

        target_pile = self.charging_piles[index]
        with target_pile.lock:
            if target_pile.current_vehicle is None:
                target_pile.current_vehicle = vehicle
                vehicle.start_time = self.vir.now()
                logging.info(f"车辆 {vehicle.vid} 开始充电（桩{index}）")
            elif len(target_pile.waiting_queue) < target_pile.queue_limit:
                target_pile.waiting_queue.append(vehicle)
                logging.info(f"车辆 {vehicle.vid} 加入桩{index}等待队列（位置：{len(target_pile.waiting_queue)}）")
            else:
                logging.info(f"桩{index}等待队列已满，车辆 {vehicle.vid} 无法加入")
                return False
        return True

    def has_available(self):
        tCar = Car(0, 0, "T",0,  0)
        fCar = Car(0, 0, "F",0,  0)
        return self.find_pile(tCar) >= 0 or self.find_pile(fCar) >= 0

    def stop_pile(self, pile_id: str):
        for index, pile in enumerate(self.charging_piles):
            if pile.id == pile_id:
                with pile.lock:
                    v = []
                    if pile.current_vehicle is not None:
                        vehicle = pile.current_vehicle
                        logging.info(f"车辆 {vehicle.vid} 在桩{pile.id}充电中断，生成报表")
                        speed = self.slow_speed if pile.mode == "T" else self.fast_speed
                        self.report_queue.put(ChargeResult(pile.id, self.vir.now(), speed, vehicle))
                        pile.current_vehicle = None
                        vehicle.charge_degree = 0
                        vehicle.charge_duration = 0
                        v.append(vehicle)
                    if len(pile.waiting_queue) > 0:
                        v.extend(pile.waiting_queue)
                        pile.waiting_queue = []
                    reschedule = self.reschedule_t if pile.mode == 'T' else self.reschedule_f
                    for _, car in enumerate(v):
                        reschedule.put(car)
                    pile.open = False
                    # 此步acquire对于本pile
                    # 某个充电桩暂停后，其无法再提供（未使用位置数量）个的可acquire信号量
                    to_acquire = pile.queue_limit + 1 - len(v)
                    acquired = 0
                    not_full = self.not_full_f if pile.mode == 'F' else self.not_full_t
                    # 如果acquire成功，相当于直接减少
                    for _ in range(to_acquire):
                        if not_full.acquire(blocking=False):
                            acquired += 1
                    # 否则，通过减少release的方式降低信号量大小
                    self.not_release_cause_stop += (to_acquire - acquired)
                return {"message:暂停成功"}
        return {"message:不存在对应的充电桩"}



    def charging_worker(self, interval=1):
        """充电桩工作线程"""
        while True:
            logging.debug("充电区线程开始工作")
            for index, pile in enumerate(self.charging_piles):
                if not pile.open:
                    continue
                with pile.lock:
                    logging.debug(f"检查充电桩:{index}")
                    if pile.current_vehicle is None:
                        logging.debug(f"该充电桩当前未在充电")
                        if not pile.waiting_queue:
                            logging.debug("该充电桩当前无排队车辆")
                            continue
                        logging.debug(f"正在调度新车辆")
                        next_vehicle = pile.waiting_queue.popleft()
                        next_vehicle.start_time = self.vir.now()
                        pile.current_vehicle = next_vehicle
                        logging.debug(f"新车辆 {pile.current_vehicle.vid} 开始充电")
                    vehicle = pile.current_vehicle
                    logging.info(f"桩 {pile.id} 为等待车辆 {vehicle.vid} 充电")
                    speed = self.slow_speed if pile.mode == "T" else self.fast_speed
                    time_passed = (interval / 3600) * time_factor
                    if vehicle.remain_time > time_passed:
                        vehicle.remain_time -= time_passed
                        vehicle.charge_duration += time_passed
                        vehicle.required -= time_passed * speed
                        vehicle.charge_degree += time_passed * speed
                    else:
                        vehicle.charge_duration += vehicle.remain_time
                        vehicle.charge_degree += vehicle.remain_time * speed
                        vehicle.remain_time = 0
                        vehicle.required = 0
                    # 空出位置，通知等待区
                    if vehicle.remain_time <= 0:
                        logging.info(f"车辆 {vehicle.vid} 在桩{pile.id}充电完成")
                        pile.current_vehicle = None
                        self.report_queue.put(ChargeResult(pile.id, self.vir.now(), speed, vehicle))
                        # 通过减少release的方式降低信号量大小
                        if self.not_release_cause_stop > 0:
                            self.not_release_cause_stop -= 1
                        else:
                            if vehicle.mode == 'T':
                                self.not_full_t.release()
                            else:
                                self.not_full_f.release()
            time.sleep(interval)


    def get_pile_status(self, index):
        """获取充电桩状态"""
        pile = self.charging_piles[index]
        return {
            "current": pile.current_vehicle.vid if pile.current_vehicle else None,
            "waiting": [v.vid for v in pile.waiting_queue],
            "queue_size": len(pile.waiting_queue)
        }

    def cal_remain_time(self, type, power):
        """计算剩余充电时间"""
        return power / (self.slow_speed if type == "T" else self.fast_speed)


class ChargingPile:
    def __init__(self, mode: str, wait_queue_length: int, id: int):
        self.mode = mode
        self.id = mode + str(id)
        self.current_vehicle = None
        self.queue_limit = wait_queue_length
        self.waiting_queue = deque()
        self.lock = threading.Lock()
        self.open = True

    def __deepcopy__(self, memo):
        # 跳过锁的拷贝
        new_pile = ChargingPile(self.mode, self.queue_limit, -1)
        new_pile.id = self.id
        new_pile.current_vehicle = copy.deepcopy(self.current_vehicle, memo)
        new_pile.waiting_queue = copy.deepcopy(self.waiting_queue, memo)
        return new_pile

    def to_dict(self):
        """安全转换为字典的方法"""
        with self.lock:
            return {
                "id": self.id,
                "mode": self.mode,
                "current": self.current_vehicle.to_dict() if self.current_vehicle else None,
                "waiting_queue": [v.to_dict() for v in self.waiting_queue]
            }
