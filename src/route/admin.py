from fastapi import APIRouter

from database import user, bill

router = APIRouter(
    prefix="/admin"
)


@router.get("/users")
async def users():
    return user.get_all()


@router.get("/bills")
async def bills():
    return bill.get_all()
