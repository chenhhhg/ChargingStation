from database.connect import connect

def get_all_bill(user_id):
    bills = connect.cursor.execute("""
        SELECT * FROM bill 
        WHERE user_id = ?
    """, (user_id,)).fetchall()
    return {"code":1, "data":bills}


def get_all():
    bills = connect.cursor.execute("""
        SELECT * FROM bill 
    """).fetchall()
    return {"code": 1, "data": bills}


def insert_bill_record(
        bill_ls: str,
        user_id: int,
        car_id: str,
        bill_date: str,
        pile_id: int,
        charge_amount: float,
        charge_duration: float,
        start_time: float,
        end_time: float,
        total_charge_fee: float,
        total_service_fee: float,
        total_fee: float,
        pay_state: int
) -> None:
    """
    插入充电账单记录
    :param bill_ls: 流水号
    :param user_id: 用户ID
    :param car_id: 车牌号
    :param bill_date: 账单日期（格式：YYYY-MM-DD HH:MM:SS）
    :param pile_id: 充电桩ID
    :param charge_amount: 充电量（度）
    :param charge_duration: 充电时长（小时）
    :param start_time: 开始时间戳
    :param end_time: 结束时间戳
    :param total_charge_fee: 充电费用
    :param total_service_fee: 服务费用
    :param total_fee: 总费用
    :param pay_state: 支付状态（0-未支付，1-已支付）
    """
    sql = '''
    INSERT INTO bill (
        bill_ls, user_id, car_id, bill_date,
        pile_id, charge_amount, charge_duration, start_time,
        end_time, total_charge_fee, total_service_fee,
        total_fee, pay_state
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    params = (
        bill_ls, user_id, car_id, bill_date,
        pile_id, charge_amount, charge_duration, start_time,
        end_time, total_charge_fee, total_service_fee,
        total_fee, pay_state
    )
    connect.cursor.execute(sql, params)
    connect.conn.commit()
