from database.connect import connect


def insert_or_update_pile_report(
        pile_id: int,
        date: str,
        total_charge_num: int,
        total_charge_time: float,
        total_charge_degree: float,
        total_charge_fee: float,
        total_service_fee: float
) -> None:
    """
    插入/更新充电桩日报表记录（假设存在自增主键id）
    :param pile_id: 充电桩ID
    :param date: 统计日期（ISO格式：YYYY-MM-DD）
    :param total_charge_num: 当日充电次数
    :param total_charge_time: 当日总充电时长（小时）
    :param total_charge_degree: 当日总充电量（度）
    :param total_charge_fee: 当日充电费用总和
    :param total_service_fee: 当日服务费用总和

    基于(pile_id, date)的唯一约束进行冲突处理
    """
    sql = """
        INSERT INTO pile_report (
            pile_id, date, total_charge_num, total_charge_time,
            total_charge_degree, total_charge_fee, total_service_fee
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(pile_id, date) DO UPDATE SET
            total_charge_num = pile_report.total_charge_num + excluded.total_charge_num,
            total_charge_time = pile_report.total_charge_time + excluded.total_charge_time,
            total_charge_degree = pile_report.total_charge_degree + excluded.total_charge_degree,
            total_charge_fee = pile_report.total_charge_fee + excluded.total_charge_fee,
            total_service_fee = pile_report.total_charge_fee + excluded.total_service_fee
        """
    params = (
        pile_id,
        date,
        total_charge_num,
        total_charge_time,
        total_charge_degree,
        total_charge_fee,
        total_service_fee
    )
    connect.cursor.execute(sql, params)
    connect.conn.commit()


def get_all():
    return connect.cursor.execute('''
        select * from pile_report
    ''').fetchall()
