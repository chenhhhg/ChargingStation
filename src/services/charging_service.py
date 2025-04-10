from core import state

def process_charging_queue():
    completed = []

    # 遍历所有充电桩
    for pile_id, queue in state.charging_piles.items():
        if not queue:
            continue

        car = queue[0]  # 当前正在充电的车辆
        speed = state.pile_speed[pile_id]
        charged = car.get("charged", 0)
        required = car["request_power"]

        # 本轮充电
        charged += speed  # 假设每次处理相当于 1 小时充电
        car["charged"] = charged

        if charged >= required:
            # 完成充电，生成记录
            state.charging_records.append({
                "car_id": car["id"],
                "pile_id": pile_id,
                "power": required,
                "time": round(required / speed, 2)
            })
            queue.pop(0)
            completed.append(car["id"])

    return {
        "message": f"本轮充电处理完成，共完成 {len(completed)} 辆车",
        "finished": completed
    }
