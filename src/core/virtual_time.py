import datetime
import threading
import time

time_factor = 60
interval = 0.1
class VirtualTime:
    def __init__(self):
        self.begin_time = datetime.datetime.now().timestamp()
        self.cur = self.begin_time
        self.worker_thread = threading.Thread(target=self.accumulator, daemon=True)

    def start(self):
        self.worker_thread.start()

    def accumulator(self):
        while True:
            time.sleep(interval)
            self.cur += time_factor * interval

    def now(self):
        return datetime.datetime.fromtimestamp(self.cur)