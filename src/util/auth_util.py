from typing import Optional
import jwt
import datetime
from hashlib import sha256
import random
import string

SECRET_KEY = "hello_world"
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 72
provinces = ['京', '沪', '津', '渝', '冀', '豫', '云', '辽', '黑', '湘',
                 '皖', '鲁', '新', '苏', '浙', '赣', '鄂', '桂', '甘', '晋',
                 '蒙', '陕', '吉', '闽', '贵', '粤', '青', '藏', '川', '宁',
                 '琼']
letters = [c for c in string.ascii_uppercase if c not in ['I', 'O']]

def generate_license_plate(num_plates=1):
    plates = []
    for _ in range(num_plates):
        # 新能源车牌格式：省份 + 字母 + (D/F) + 5位字母/数字
        province = random.choice(provinces)
        char = random.choice(letters)
        energy_type = random.choice(['D', 'F'])  # D: 纯电, F: 混动
        suffix = ''.join(random.choices(string.digits + ''.join(letters), k=5))
        plate = f"{province}{char}{energy_type}{suffix}"
        plates.append(plate)

    return plates if num_plates > 1 else plates[0]

def generate_token(user_id: int, car_id: str) -> Optional[str]:
    now_utc = datetime.datetime.now(datetime.UTC)
    payload = {
        "user_id": user_id,
        "car_id":car_id,
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
    # if now_utc > exp:
    #     print('token已失效')
    #     return False, 'token已失效，请重新登录'
    return True, {"user_id":data.pop('user_id'),"car_id":data.pop('car_id')}

def hash_password(password):
    return sha256(password.encode()).hexdigest()

if __name__ == '__main__':
    for _ in range(10):
        t = generate_token(_, generate_license_plate())
        print(f"\"{t}\"")
        decode_token(t)