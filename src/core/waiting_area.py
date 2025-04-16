import copy
import heapq
import threading
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

class WaitingArea:
    def __init__(self, charging_zone, semaphore: threading.Semaphore, max_size=5):
        # 依赖注入充电区实例
        self.charging_zone = charging_zone
        self.semaphore = semaphore
        self.wait_semaphore = threading.Semaphore(0)
        # 等待队列配置
        self.max_waiting = max_size
        self.waiting_heap = []
        self.waiting_lock = threading.Lock()
        self.waiting_cond = threading.Condition()

        # 启动调度线程
        self.worker_thread = threading.Thread(target=self._dispatch_worker, daemon=True)

    def start(self):
        self.worker_thread.start()

    def get_state(self):
        return copy.deepcopy(self.waiting_heap)

    def add_vehicle(self, vehicle):
        """添加车辆到优先队列"""
        with self.waiting_lock:
            if len(self.waiting_heap) >= self.max_waiting:
                logging.info(f"车辆 {vehicle.vid} 等待队列已满")
                return False
            heapq.heappush(self.waiting_heap, vehicle)
            logging.info(f"车辆 {vehicle.vid} 加入等待区")

        # 通知调度线程
        self.wait_semaphore.release()
        return True

    def _dispatch_worker(self):
        """调度工作线程（内部方法）"""
        while True:
            self.semaphore.acquire()
            self.wait_semaphore.acquire()
            # 获取最高优先级车辆
            with self.waiting_lock:
                vehicle = heapq.heappop(self.waiting_heap)

            # 尝试分配充电桩
            if self.charging_zone.assign_vehicle(vehicle):
                logging.info(f"车辆 {vehicle.vid} 已分配充电桩")
            else:
                logging.info(f"车辆 {vehicle.vid} 分配失败，重新加入队列")
                self.add_vehicle(vehicle)

    @property
    def queue_size(self):
        """当前等待队列长度"""
        with self.waiting_lock:
            return len(self.waiting_heap)
