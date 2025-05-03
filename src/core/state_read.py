from core.state_const import VehicleStatus

charging_zone = None
waiting_zone = None
vir = None

def get_all_state():
    piles = charging_zone.get_state()
    waiting_cars = waiting_zone.get_state()
    return {
        "time":vir.now(),
        "waiting_area":waiting_cars,
        "charging_area":piles
    }

def get_user_state(user_id:int):
    if waiting_zone.check_if_rescheduling(user_id):
        return VehicleStatus.PENDING_RESCHEDULE
    waiting_cars = waiting_zone.get_state()
    if waiting_cars is None:
        return VehicleStatus.LOGGED_IN
    wt = waiting_cars["T"]
    wf = waiting_cars["F"]
    for _, car in enumerate(wt):
        if car.uid == user_id:
            return VehicleStatus.WAITING
    for _, car in enumerate(wf):
        if car.uid == user_id:
            return VehicleStatus.WAITING
    piles = charging_zone.get_state()
    for _, pile in enumerate(piles):
        if pile["current"] is not None and pile["current"]["uid"] == user_id:
            return VehicleStatus.CHARGING
        for _, car in enumerate(pile["waiting_queue"]):
            if car["uid"] == user_id:
                return VehicleStatus.QUEUED
    return VehicleStatus.LOGGED_IN

