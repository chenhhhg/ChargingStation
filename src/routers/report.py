from fastapi import APIRouter
from services.report_service import get_report

router = APIRouter()

@router.get("/stat")
def get_statistics():
    return get_report()
