from fastapi import APIRouter
from services.charging_service import process_charging_queue

router = APIRouter()

@router.post("/process")
def process_charging():
    return process_charging_queue()
