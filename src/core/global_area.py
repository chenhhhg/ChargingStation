class Car:
    def __init__(self, uid, vid, mode, required_charge, remain_time):
        self.uid = uid
        self.vid = vid
        self.mode = mode
        self.required = required_charge
        self.remain_time = remain_time
        self.start_time = None
        self.charge_duration = 0
        self.charge_degree = 0
        self.number = None
    def __lt__(self, other):
        return self.remain_time < other.remain_time

    def to_dict(self):
        return {
            "uid": self.uid,
            "vid": self.vid,
            "mode": self.mode,
            "required":self.required,
            "remain_time":self.remain_time,
            "charge_duration": self.charge_duration,
            "charge_degree": self.charge_degree,
            "start_time": self.start_time,
            "number": self.number,
        }

class ChargeResult(Car):
    def __init__(self, pile_id, end_time, speed, car: Car, pile):
        super().__init__(car.uid, car.vid, car.mode, car.required, car.remain_time)  # 调用父类构造函数
        self.pile_id = pile_id          # 充电桩编号
        self.pile = pile
        self.end_time = end_time        # 充电结束时间
        self.start_time = car.start_time
        self.charge_duration = car.charge_duration
        self.speed = speed
        self.charge_degree = car.charge_degree
