from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
from core import state_read
from route.__init__ import login_required

router = APIRouter(
    prefix="/system"
)

@router.get("/global")
def global_message():
    return state_read.get_all_state()