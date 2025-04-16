from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
from services import waiting_service
from route.__init__ import login_required
from database import user, bill
from util import auth_util

router = APIRouter(
    prefix="/user"
)

class LoginUser(BaseModel):
    user_name: str
    password: str

class RegisterUser(LoginUser):
    capacity: int

@router.post("/login")
async def user_login(login_user: LoginUser, response: Response):
    """用户登录"""
    print(login_user.user_name, "login")
    """验证用户名密码"""
    info = user.login(login_user.user_name, login_user.password)
    if info['code'] == 1:
        data = info['data']
        response.headers["Authorization"] = auth_util.generate_token(info['data']['user_id'], info['data']['car_id'])
    return info

@router.post("/register")
async def user_register(register_user: RegisterUser):
    return user.register(register_user.user_name, register_user.password, register_user.capacity)

@router.post("/charge")
@login_required
async def request_charge(request: Request, type: str, power: int):
    #todo check state
    car_id = request.state.car_id
    return waiting_service.add_vehicle(car_id, type, power)

@router.post("/charge/type")
@login_required
async def request_charge(request: Request, type: str):
    #todo check state
    car_id = request.state.car_id
    user_id = request.state.user_id


@router.get("/bills")
@login_required
async def bills(request: Request):
    return bill.get_all_bill(request.state.user_id)

