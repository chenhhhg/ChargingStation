charging_zone = None
waiting_zone = None

def get_all_state():
    piles = charging_zone.get_state()
    waiting_cars = waiting_zone.get_state()
    return {
        "waiting_area":waiting_cars,
        "charging_area":piles
    }
