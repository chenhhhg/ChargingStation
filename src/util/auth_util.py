from typing import Optional
import jwt
import datetime
from hashlib import sha256

SECRET_KEY = "hello_world"
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 72


def generate_token(user_id: int) -> Optional[str]:
    now_utc = datetime.datetime.now(datetime.UTC)
    payload = {
        "user_id": user_id,
        "exp": now_utc + datetime.timedelta(hours=TOKEN_EXPIRE_HOURS)
    }
    # 生成令牌（确保密钥为字节串）
    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return token

def decode_token(token):
    if token is None:
        return False, "token为空"
    try:
        data = jwt.decode(token, key=SECRET_KEY, algorithms=JWT_ALGORITHM)
    except jwt.exceptions.InvalidTokenError:
        print("token解析失败")
        return False, "token解析失败"
    exp = data.pop('exp')
    now_utc = datetime.datetime.now(datetime.UTC)
    if now_utc > exp:
        print('token已失效')
        return False, 'token已失效，请重新登录'
    return True, data.pop('user_id')

def hash_password(password):
    return sha256(password.encode()).hexdigest()