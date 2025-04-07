import sqlite3

class Connection:
    def __init__(self):
        """打开/创建数据库"""
        self.conn = sqlite3.connect('charging_station.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        print("数据库打开成功")
        self.cursor = self.conn.cursor()
        self.create_bill_table()
        self.create_user_table()
        self.create_pile_table()

    def close_db(self):
        self.conn.close()

    def __del__(self):
        print("数据库关闭成功")
        self.conn.close()

    def create_bill_table(self):
        # 时间(日、周、月)、充电桩编号、累计充电次数、累计充电时长、累计充电量、累计充电费用、累计服务费用、累计总费用
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS bill
           (bill_id          Integer PRIMARY KEY,
           bill_ls           TEXT,
           user_id           Integer,
           car_id            TEXT     NOT NULL,
           bill_date         TEXT    NOT NULL,
           pile_id           Integer    NOT NULL,
           charge_amount     REAL    NOT NULL,
           charge_duration     REAL    NOT NULL,
           start_time         REAL    NOT NULL,
           end_time         REAL    NOT NULL,
           total_charge_fee         REAL    NOT NULL,
           total_service_fee         REAL    NOT NULL,
           total_fee         REAL    NOT NULL,
           pay_state         Integer      NOT NULL);
                       ''')
        print("bill数据表创建成功")
        self.conn.commit()

    def create_user_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                user_id         INTEGER  PRIMARY KEY,   -- 自增主键（无需 AUTOINCREMENT）
                user_name       TEXT     NOT NULL UNIQUE,  -- 用户名（唯一）
                password_hash   TEXT     NOT NULL,      -- 密码哈希值（非明文）
                car_id          TEXT     NOT NULL,      -- 车辆标识
                capacity        REAL     NOT NULL CHECK (capacity >= 0)  -- 容量（非负）
            );
       ''')
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_name ON user (user_name);
        ''')
        print("user数据表创建成功")
        self.conn.commit()

    def create_pile_table(self):
        #是否正常工作、系统启动后累计充电次数、充电总时长、充电总电量
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pile_report(
            pile_id Integer,
            date DATE NOT NULL,
            total_charge_num INTEGER NOT NULL,
            total_charge_time DOUBLE NOT NULL,
            total_capacity DOUBLE NOT NULL,
            total_charge_fee DOUBLE NOT NULL,
            total_service_fee DOUBLE NOT NULL,
            primary key (pile_id,date)
            );
                        """)
        print("pile_report表格创建成功")
        self.conn.commit()

connect = Connection()