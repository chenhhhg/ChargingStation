import array
import queue
import threading
from datetime import datetime

from core.global_area import ChargeResult
from database import bill

'''
CREATE TABLE IF NOT EXISTS bill
           (bill_id          Integer PRIMARY KEY,
           bill_ls           TEXT,
           user_id           Integer,
           car_id            TEXT     NOT NULL,
           bill_date         TEXT    NOT NULL,
           pile_id           Integer    NOT NULL,
           charge_amount     REAL    NOT NULL,
           charge_duration     REAL    NOT NULL,
           start_time         REAL    NOT NULL,
           end_time         REAL    NOT NULL,
           total_charge_fee         REAL    NOT NULL,
           total_service_fee         REAL    NOT NULL,
           total_fee         REAL    NOT NULL,
           pay_state         Integer      NOT NULL);
                       )
'''


peak_time = [10, 11, 12, 13, 14, 18, 19, 20]
off_peak_time = [23, 0, 1, 2, 3, 4, 5, 6]

class FeeConfig:
    def __init__(self, PeakRate, NormalRate, OffPeakRate, ServiceFeeRate):
        self.PeakRate = PeakRate
        self.NormalRate = NormalRate
        self.OffPeakRate = OffPeakRate
        self.ServiceFeeRate = ServiceFeeRate

class Reporter:
    def __init__(self, report_queue: queue.Queue, factor, config:FeeConfig):
        self.report_queue = report_queue
        self.worker_thread = threading.Thread(target=self.cal_and_generate, daemon=True)
        self.factor = factor
        self.config = config
    def start(self):
        self.worker_thread.start()
    def cal_and_generate(self):
        while True:
            result = self.report_queue.get()
            start = result.start_time
            start_hour = start.hour
            rest_min_start = 60 - start.minute
            end = result.end_time
            end_hour = end.hour
            rest_min_end = end.minute
            # 收费区间的边界，假设用左闭右开定义区间，同时对跨越一天的加24h
            bound = [7,10,18,21,23,31,34,42,45,47]
            n = self.config.NormalRate
            p = self.config.PeakRate
            o = self.config.OffPeakRate
            s = self.config.ServiceFeeRate
            fee_map = [n,p,n,n,o,n,p,n,n,o]
            if end_hour < start_hour:
                end_hour += 24

            fee = 0
            speed = result.speed

            if start_hour == end_hour and rest_min_start+rest_min_end > 60:
                t = rest_min_start + rest_min_end - 60
                index = 0
                while bound[index] < start_hour:
                    index+=1
                fee = (t / 60) * speed * (fee_map[index] + s)
            else:
                for i in range(end_hour - start_hour + 1):
                    now = i + start_hour
                    index = 0
                    while bound[index] < now:
                        index+=1
                    fee += speed * 1 * (fee_map[index] + s)

                    if now == start_hour:
                        fee += (rest_min_start / 60) * speed * (fee_map[index] + s)
                    if now == end_hour :
                        fee += (rest_min_end / 60) * speed * (fee_map[index] + s)

            print(fee)