from fastapi import APIRouter
from services.time_service import get_virtual_time, update_virtual_time

router = APIRouter()

@router.get("/now")
def now():
    return get_virtual_time()

@router.post("/set")
def set_time(factor: float):
    return update_virtual_time(factor)
