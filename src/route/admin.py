from fastapi import APIRouter

from core.global_area import Car
from core.state_const import VehicleStatus
from core.state_read import get_user_state
from database import user, bill, pile

router = APIRouter(
    prefix="/admin"
)

charging_area = None
waiting_zone = None

@router.get("/users")
async def users():
    return user.get_all()


@router.get("/bills")
async def bills():
    return bill.get_all()


@router.post("/stop")
async def stop(pile_id: str):
    return charging_area.stop_pile(pile_id)


@router.post("/open")
async def open(pile_id: str):
    return charging_area.open_pile(pile_id)


@router.get("/piles")
async def piles():
    return pile.get_all()

@router.post("/test/add/user")
def test_add_user():
    return user.test_add()

@router.post("/test/add/charge")
def test_add_charge():
    for i in range(10):
        name = "test"+str(i)
        u = user.get_by_name(name)
        if u is None:
            continue
        mode = "T"
        user_id = u["user_id"]
        state = get_user_state(user_id)
        if state != VehicleStatus.LOGGED_IN:
            continue

        car_id = u["car_id"]
        remain_time = charging_area.cal_remain_time(mode, 120)
        waiting_zone.add_vehicle(Car(user_id, car_id, mode, 120, remain_time))