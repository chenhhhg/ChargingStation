from fastapi import APIRouter
from services.state_service import get_system_state

router = APIRouter()

@router.get("/show")
def show_system_state():
    return get_system_state()
