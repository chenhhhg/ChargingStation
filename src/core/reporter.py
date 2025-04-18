import queue
import threading

from database import bill

peak_time = [10, 11, 12, 13, 14, 18, 19, 20]
off_peak_time = [23, 0, 1, 2, 3, 4, 5, 6]


class SerialGenerator:
    def __init__(self):
        self.current = 0
        self.lock = threading.Lock()
        self.current_date = None
        self.vir = None

    def get_serial(self):
        with self.lock:
            now_date = self.vir.now()
            if now_date != self.current_date:
                self.current_date = now_date
                self.current = 0
            self.current += 1
            return f"LS{self.current_date}{self.current:04d}"
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
        self.vir = None
        self.serial_gen = SerialGenerator()
    def start(self):
        self.serial_gen.vir = self.vir
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

            fee_charge = 0
            fee_service = 0
            speed = result.speed

            # 规定充电时间不多与24h
            # 充电时间小于1h
            if start_hour == end_hour and rest_min_start+rest_min_end > 60:
                t = rest_min_start + rest_min_end - 60
                index = 0
                while bound[index] < start_hour:
                    index+=1
                fee_charge = (t / 60) * speed * fee_map[index]
                fee_service = (t / 60) * speed * s
            # 充电时间大于1h
            else:
                for i in range(end_hour - start_hour + 1):
                    now = i + start_hour
                    index = 0
                    while bound[index] < now:
                        index+=1
                    fee_charge += speed * 1 * fee_map[index]
                    fee_service += speed * 1 * s
                    if now == start_hour:
                        fee_charge += (rest_min_start / 60) * speed * fee_map[index]
                        fee_service += (rest_min_start / 60) * speed * s
                    if now == end_hour :
                        fee_charge += (rest_min_end / 60) * speed * fee_map[index]
                        fee_service += (rest_min_end / 60) * speed * s
            bill_ls = self.serial_gen.get_serial()
            bill.insert_bill_record(bill_ls=bill_ls, user_id=result.uid, car_id=result.vid, bill_date=self.vir.now(),
                                    pile_id=result.pile_id, charge_amount=result.charge_degree,
                                    charge_duration=result.charge_duration,
                                    start_time=start, end_time=end, total_charge_fee=fee_charge,
                                    total_service_fee=fee_service,
                                    total_fee=fee_service + fee_charge, pay_state=0)
