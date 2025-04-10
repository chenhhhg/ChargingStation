from fastapi import APIRouter
from services.waiting_service import call_next_vehicle
from core.state import waiting_area

router = APIRouter()

@router.post("/call")
def call_next():
    return call_next_vehicle()

@router.post("/add")
def add_vehicle(vehicle_id: str, mode: str, request_power: float):
    if len(waiting_area) >= 6:
        return {"message": "等候区已满"}

    prefix = "F" if mode == "fast" else "T"
    waiting_area.append({
        "id": f"{prefix}{vehicle_id}",
        "mode": mode,
        "request_power": request_power
    })

    return {"message": f"车辆 {prefix}{vehicle_id} 已加入等候队"}
