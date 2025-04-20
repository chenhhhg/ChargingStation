import copy
import heapq
import logging
import threading
import time

from core.state_const import VehicleStatus

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

class WaitingArea:
    def __init__(self, charging_zone, semaphore_t: threading.Semaphore, semaphore_f: threading.Semaphore, max_size=5):
        # 依赖注入充电区实例、信号量通信
        self.charging_zone = charging_zone
        self.not_full_t = semaphore_t
        self.not_full_f = semaphore_f
        # 等待队列配置
        self.max_waiting = max_size
        self.waiting_heap_t = []
        self.waiting_heap_f = []
        self.waiting_lock = threading.Lock()
        self.waiting_cond = threading.Condition()

        self.worker_thread = threading.Thread(target=self._dispatch_worker, daemon=True)

        self.reschedule_t = None
        self.reschedule_f = None

        self.count_t = 0
        self.count_f = 0
    def start(self):
        self.worker_thread.start()

    def get_state(self):
        return {"T": copy.deepcopy(self.waiting_heap_t), "F": copy.deepcopy(self.waiting_heap_f),
                "T重新调度队列": self.reschedule_t.qsize(), "F重新调度队列": self.reschedule_f.qsize()
                }

    def add_vehicle(self, vehicle):
        """添加车辆到优先队列"""
        with self.waiting_lock:
            if len(self.waiting_heap_t) + len(self.waiting_heap_f) >= self.max_waiting:
                logging.debug(f"车辆 {vehicle.vid} 等待队列已满")
                return False
            if vehicle.mode == "T":
                vehicle.number = self.count_t
                self.count_t += 1
                heapq.heappush(self.waiting_heap_t, vehicle)
            else:
                vehicle.number = self.count_f
                self.count_f += 1
                heapq.heappush(self.waiting_heap_f, vehicle)
            logging.debug(f"车辆 {vehicle.vid} 加入等待区, 模式:{vehicle.mode}")
        return True

    def pop_all(self, q, exclude=None):
        temp = []
        while not q.empty():
            car = q.get()
            if car != exclude:
                temp.append(car)
        return temp

    def check_if_rescheduling(self, user_id):
        rescheduling = False
        with self.waiting_lock:
            temp = self.pop_all(self.reschedule_t)
            for _, car in enumerate(temp):
                rescheduling = not rescheduling and car.uid == user_id
                self.reschedule_t.put(car)
            if rescheduling:
                return True
            temp = self.pop_all(self.reschedule_f)
            for _, car in enumerate(temp):
                rescheduling = not rescheduling and car.uid == user_id
                self.reschedule_f.put(car)
            return rescheduling

    def cancel(self, user_id, state: VehicleStatus):
        if state == VehicleStatus.PENDING_RESCHEDULE:
            with self.waiting_lock:
                temp = self.pop_all(self.reschedule_t)
                for _, car in enumerate(temp):
                    if car.uid != user_id:
                        self.reschedule_t.put(car)
                temp = self.pop_all(self.reschedule_f)
                for _, car in enumerate(temp):
                    if car.uid != user_id:
                        self.reschedule_f.put(car)
                return {"message:取消成功"}

        with self.waiting_lock:
            vehicle = None
            for _, car in enumerate(self.waiting_heap_t):
                if car.uid == user_id:
                    vehicle = car
            for _, car in enumerate(self.waiting_heap_f):
                if car.uid == user_id:
                    vehicle = car
            if vehicle == None:
                return {"message:错过了，车去充电了"}
            if vehicle.mode == 'T':
                self.waiting_heap_t.remove(vehicle)
            else:
                self.waiting_heap_f.remove(vehicle)
            return {"message:取消成功"}

    def modify_vehicle(self, user_id, mode, power, cal_func):
        with self.waiting_lock:
            vehicle = None
            for _, car in enumerate(self.waiting_heap_t):
                if car.uid == user_id:
                    vehicle = car
            for _, car in enumerate(self.waiting_heap_f):
                if car.uid == user_id:
                    vehicle = car
            if vehicle == None:
                return {"message:错过了，车去充电了"}
            if mode == vehicle.mode and power == vehicle.required:
                return {"message:新旧值相同"}
            if vehicle.mode == 'T':
                self.waiting_heap_t.remove(vehicle)
            else:
                self.waiting_heap_f.remove(vehicle)
            mode = vehicle.mode if mode == 'D' else mode
            vehicle.mode = mode
            vehicle.required = power
            vehicle.remain_time = cal_func(mode, power)
            if mode == 'T':
                heapq.heappush(self.waiting_heap_t, vehicle)
            else:
                heapq.heappush(self.waiting_heap_f, vehicle)
            return {"message:成功修改"}



    def _dispatch_worker(self, interval=1):
        """调度工作线程（内部方法）"""
        while True:
            logging.debug("等候区线程开始工作")
            with self.waiting_lock:
                logging.debug("尝试调度T车辆，优先调度需要重新调度的车辆")
                while self.reschedule_t.qsize() > 0 and self.not_full_t.acquire(blocking=False):
                    vehicle = self.reschedule_t.get()
                    self.charging_zone.assign_vehicle(vehicle)
                    logging.debug(f"车辆 {vehicle.vid} 模式 {vehicle.mode} 已分配充电桩")
                if self.waiting_heap_t and self.not_full_t.acquire(blocking=False):
                    vehicle = heapq.heappop(self.waiting_heap_t)
                    self.charging_zone.assign_vehicle(vehicle)
                    logging.debug(f"车辆 {vehicle.vid} 模式 {vehicle.mode} 已分配充电桩")
                logging.debug("尝试调度F车辆，优先调度需要重新调度的车辆")
                while self.reschedule_f.qsize() > 0 and self.not_full_f.acquire(blocking=False):
                    vehicle = self.reschedule_f.get()
                    self.charging_zone.assign_vehicle(vehicle)
                    logging.debug(f"车辆 {vehicle.vid} 模式 {vehicle.mode} 已分配充电桩")
                if self.waiting_heap_f and self.not_full_f.acquire(blocking=False):
                    vehicle = heapq.heappop(self.waiting_heap_f)
                    self.charging_zone.assign_vehicle(vehicle)
                    logging.debug(f"车辆 {vehicle.vid} 模式 {vehicle.mode} 已分配充电桩")
            time.sleep(interval)

    @property
    def queue_size(self):
        """当前等待队列长度"""
        with self.waiting_lock:
            return len(self.waiting_heap_t) + len(self.waiting_heap_f)
