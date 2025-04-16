from fastapi import APIRouter
from services.fault_service import handle_fault

router = APIRouter()

@router.post("/report")
def report_fault(pile_id: str):
    return handle_fault(pile_id)
