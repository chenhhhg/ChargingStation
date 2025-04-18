from fastapi import APIRouter

from core import charging_area
from database import user, bill, pile

router = APIRouter(
    prefix="/admin"
)

charging_area = None

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
