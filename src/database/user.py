from database.connect import connect
from util import auth_util

class User:
    user_id:int
    user_name:str
    car_id:str
    capacity:int

def login(user_name: str, password: str):
    user_data = get_by_name(user_name)
    if not user_data:
        return {"code": 0, "message": "用户未注册"}
    # 验证密码哈希（假设数据库中存储的是哈希值）
    input_password_hash = auth_util.hash_password(password)
    if input_password_hash == user_data["password_hash"]:
        return {
            "code": 1,
            "message": "登录成功",
            "data": {
                "user_id":user_data["user_id"],
                "car_id":user_data["car_id"]
            }
        }
    else:
        return {"code": 0, "message": "密码不正确"}

def register(user_name: str, password: str, capacity: int):
    if get_by_name(user_name):
        return {"code":0, "message": "用户名已存在！"}
    insert(capacity, password, user_name)
    return {"code":1, "message":"注册成功"}


def insert(capacity, password, user_name):
    connect.cursor.execute("""
        INSERT INTO user
        (user_name, password_hash, car_id, capacity)
        VALUES
        (?, ?, ?, ?) """
                           , (user_name, auth_util.hash_password(password), auth_util.generate_license_plate(), capacity
                              )
                           )
    connect.conn.commit()
def get_by_name(user_name:str):
    cursor = connect.cursor.execute("""
            SELECT user_id, user_name, password_hash, car_id, capacity
            FROM user
            WHERE user_name = ?
            LIMIT 1 """,
                                    (user_name,)
        )
    return cursor.fetchone()
def get_by_id(user_id):
    cursor = connect.cursor.execute("""
                SELECT user_id, user_name, password_hash, car_id, capacity
                FROM user
                WHERE user_id = ?
                LIMIT 1 """,
                                    (user_id,)
                                    )
    return cursor.fetchone()