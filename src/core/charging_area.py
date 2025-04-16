import copy
import queue
import threading
import time
import logging
from datetime import datetime
from collections import deque
from core.global_area import Car, ChargeResult

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

class ChargingZone:
    def __init__(self, num_piles, semaphore: threading.Semaphore, report_queue: queue.Queue,
                 fast_pile_rate=0.3, fast_speed=30, slow_speed=7, wait_queue_length=1):
        self.waiting_cond = None
        self.charging_piles = []
        self.fast_pile_rate = fast_pile_rate
        self.fast_speed = fast_speed
        self.slow_speed = slow_speed
        self.report_queue = report_queue
        self.semaphore = semaphore

        # 初始化充电桩
        fast_count = int(num_piles * self.fast_pile_rate)
        self.charging_piles = [ChargingPile("T", wait_queue_length, _) for _ in range(num_piles - fast_count)]
        self.charging_piles.extend(ChargingPile("F", wait_queue_length, _) for _ in range(fast_count))

        # 启动充电工作线程
        self.worker_thread = threading.Thread(target=self.charging_worker, daemon=True)

    def start(self):
        self.worker_thread.start()

    def get_state(self):
        return [copy.deepcopy(pile.to_dict()) for pile in self.charging_piles]

    def find_pile(self, vehicle: Car):
        """寻找最优充电桩"""
        best_score = float('inf')
        best_index = -1
        for i, pile in enumerate(self.charging_piles):
            with pile.lock:
                if pile.mode != vehicle.mode or len(pile.waiting_queue) == pile.queue_limit:
                    continue
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
                vehicle.start_time = datetime.now()
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

    def charging_worker(self, interval=1):
        """充电桩工作线程"""
        while True:
            time.sleep(interval)
            logging.info("充电区线程开始工作")
            for index, pile in enumerate(self.charging_piles):
                with pile.lock:
                    logging.info(f"检查充电桩:{index}")
                    if pile.current_vehicle is None:
                        logging.info(f"该充电桩当前未在充电")
                        if not pile.waiting_queue:
                            logging.info("该充电桩当前无排队车辆")
                            continue
                        logging.info(f"正在调度新车辆")
                        next_vehicle = pile.waiting_queue.popleft()
                        next_vehicle.start_time = datetime.now()
                        pile.current_vehicle = next_vehicle
                        logging.info(f"新车辆 {pile.current_vehicle.vid} 开始充电")
                    vehicle = pile.current_vehicle
                    logging.info(f"桩{index} 开始为等待车辆 {vehicle.vid} 充电")
                    speed = self.slow_speed if pile.mode == "T" else self.fast_speed
                    charged = interval * speed
                    if vehicle.remain_time > charged:
                        vehicle.remain_time -= charged
                        vehicle.charge_duration += charged
                    else:
                        vehicle.charge_duration += vehicle.remain_time
                        vehicle.remain_time = 0
                    # 空出位置，通知等待区
                    if vehicle.remain_time <= 0:
                        charge_time = (datetime.now() - vehicle.start_time).total_seconds()
                        logging.info(f"车辆 {vehicle.vid} 在桩{index}充电完成，耗时 {charge_time:.1f}秒")
                        pile.current_vehicle = None
                        self.report_queue.put(ChargeResult(pile.id, datetime.now(), vehicle))
                        self.semaphore.release()

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

    def __deepcopy__(self, memo):
        # 跳过锁的拷贝
        new_pile = ChargingPile(self.mode)
        new_pile.current_vehicle = copy.deepcopy(self.current_vehicle, memo)
        new_pile.waiting_queue = copy.deepcopy(self.waiting_queue, memo)
        return new_pile

    def to_dict(self):
        """安全转换为字典的方法"""
        with self.lock:
            return {
                "mode": self.mode,
                "current": self.current_vehicle.to_dict() if self.current_vehicle else None,
                "waiting_queue": [v.to_dict() for v in self.waiting_queue],
                "queue_size": len(self.waiting_queue)
            }
