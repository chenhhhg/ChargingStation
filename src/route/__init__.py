import asyncio

from fastapi import HTTPException, Request, status
from functools import wraps
from typing import Callable, Any, Coroutine
from util import auth_util

def login_required(func: Callable) -> Callable[[Request], Coroutine[Any, Any, Any]]:
    """
    FastAPI JWT 登录校验装饰器
    - 自动从请求头提取 Token
    - 验证 Token 有效性
    - 将 user_id 注入请求的 `state` 中
    """
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        # 从请求头获取 Token
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="身份认证缺失"
            )

        # 解码 Token
        is_valid, result = auth_util.decode_token(token)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result  # 直接传递 decode_token 的错误消息
            )

        # 将 user_id 存入请求的 state 中
        request.state.user_id = result[0]
        request.state.car_id = result[1]

        # 执行原函数（支持同步/异步）
        if asyncio.iscoroutinefunction(func):
            return await func(request, *args, **kwargs)
        else:
            return func(request, *args, **kwargs)

    return wrapper