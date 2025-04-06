from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from route.__init__ import login_required
from database import user
from util import auth_util

router = APIRouter(
    prefix="/user"
)

class LoginUser(BaseModel):
    user_name: str
    password: str

@router.post("/login")
async def user_login(login_user: LoginUser, response: Response):
    """用户登录"""
    print(login_user.user_name, "login")
    """验证用户名密码"""
    info = user.login(login_user.user_name, login_user.password)
    if info['code'] == 1:
        response.headers["Authorization"] = auth_util.generate_token(info['data']['user_id'])
    return info

@router.get("/protected")
@login_required
async def protected_route(request: Request):
    user_id = request.state.user_id
    return {"code": 1, "message": "访问成功", "data": {"user_id": user_id}}