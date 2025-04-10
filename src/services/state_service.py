from core import state

def get_system_state():
    # 整理充电桩状态（只显示车 ID 和当前充了多少）
    pile_info = {
        pile_id: [
            {
                "id": car["id"],
                "charged": car.get("charged", 0),
                "request": car["request_power"]
            }
            for car in queue
        ]
        for pile_id, queue in state.charging_piles.items()
    }

    # 整理等候区状态
    waiting_info = [
        {
            "id": car["id"],
            "mode": car["mode"],
            "request_power": car["request_power"]
        }
        for car in state.waiting_area
    ]

    return {
        "virtual_time": state.virtual_time,
        "waiting_area": waiting_info,
        "charging_piles": pile_info,
        "charging_records": state.charging_records
    }
