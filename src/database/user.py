from database.connect import connect
from util import auth_util

def login(user_name: str, password: str):
    cursor = connect.c.execute("""
        SELECT user_id, user_name, password_hash, car_id, capacity
        FROM user
        WHERE user_name = ?
        LIMIT 1 """,
        (user_name,)
    )
    user_data = cursor.fetchone()
    if not user_data:
        return {"code": 0, "message": "用户未注册"}

        # 验证密码哈希（假设数据库中存储的是哈希值）
    input_password_hash = auth_util.hash_password(password)
    if input_password_hash == user_data["password_hash"]:
        return {
            "code": 1,
            "message": "登录成功",
            "data": {
                "user_id": user_data["user_id"],
                "user_name": user_data["user_name"],
                "car_id": user_data["car_id"],
                "car_capacity": user_data["car_capacity"]
            }
        }
    else:
        return {"code": 0, "message": "密码不正确"}