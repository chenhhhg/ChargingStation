# 快充桩（A, B），慢充桩（C, D, E）
charging_piles = {
    'A': [],  # 快充
    'B': [],
    'C': [],  # 慢充
    'D': [],
    'E': [],
}

# 每个队列最大长度为 2（只有第一个能充电）
CHARGING_QUEUE_LIMIT = 2

# 等候区：最多同时等候 6 辆车
waiting_area = []

WAITING_LIMIT = 6

# 虚拟车辆格式（示例）
# {
#     "id": "F1",
#     "mode": "fast",        # fast / slow
#     "request_power": 30,   # 请求充电量
# }
# 每桩每小时充多少度电（快充30度/小时，慢充7度/小时）
pile_speed = {
    'A': 30,
    'B': 30,
    'C': 7,
    'D': 7,
    'E': 7,
}

# 当前虚拟时间（单位：小时）
virtual_time = {
    "now": 0.0,
    "factor": 1.0  # 倍速（未用于推进，仅展示）
}

# 充电记录（可用于报表）
charging_records = []
