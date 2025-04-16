from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from route.__init__ import login_required
from database import user, bill
from util import auth_util
from core.global_area import Car
from core.state_read import get_user_state
from core.state_const import VehicleStatus

router = APIRouter(
    prefix="/user"
)

charging_zone = None
waiting_zone = None

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
        response.headers["Authorization"] = auth_util.generate_token(info['data']['user_id'], info['data']['car_id'])
    return info

@router.post("/register")
async def user_register(register_user: RegisterUser):
    return user.register(register_user.user_name, register_user.password, register_user.capacity)

@router.post("/charge")
@login_required
async def request_charge(request: Request, type: str, power: int):
    # check type and power valid
    if type != 'T' and type != 'F':
        return {f"message:参数错误{type}"}

    user_id = request.state.user_id

    state = get_user_state(user_id)

    if state != VehicleStatus.LOGGED_IN:
        return {f"message:当前状态不合法：{state.name}"}

    u = user.get_by_id(user_id)
    if u["capacity"] < power:
        return {f"message:超出电容量，最大负荷:{u["capacity"]}"}

    car_id = request.state.car_id
    remain_time = charging_zone.cal_remain_time(type, power)
    if waiting_zone.add_vehicle(Car(user_id, car_id, type, power, remain_time)):
        return {"message:成功加入等候区！耐心等待充电吧"}
    return {"message":"抱歉，现在太多人了，没办法提供充电服务了"}


@router.get("/bills")
@login_required
async def bills(request: Request):
    return bill.get_all_bill(request.state.user_id)

