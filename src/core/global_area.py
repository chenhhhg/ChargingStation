class Car:
    def __init__(self, uid, vid, mode, required_charge, remain_time):
        self.uid = uid
        self.vid = vid
        self.mode = mode
        self.required = required_charge
        self.remain_time = remain_time
        self.start_time = None

    def __lt__(self, other):
        return self.remain_time < other.remain_time

    def to_dict(self):
        return {
            "user_id": self.uid,
            "car_id": self.vid,
            "mode": self.mode,
            "required_charge":self.required,
            "remain_time":self.remain_time
        }