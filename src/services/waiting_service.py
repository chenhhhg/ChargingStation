import time

from core import state
from core.state import waiting_area
import threading

def wait_schedule(interval_sec=10):
    while True:
        call_next_vehicle()
        #todo 修改成阻塞等待阻塞队列与充电区信号量
        time.sleep(interval_sec)

def add_vehicle(vehicle_id: str, mode: str, request_power: float):
    if len(waiting_area) >= 6:
        return {"message": "等候区已满"}

    prefix = "F" if mode == "fast" else "T"
    waiting_area.append({
        "id": f"{prefix}{vehicle_id}",
        "mode": mode,
        "request_power": request_power
    })

    return {"message": f"车辆 {prefix}{vehicle_id} 已加入等候队"}

def call_next_vehicle():
    if not state.waiting_area:
        return {"message": "等候区暂无车辆"}
    #todo 修改调度算法

    # 取出队首车辆
    vehicle = state.waiting_area.pop(0)
    mode = vehicle["mode"]
    best_pile = None
    min_time = float('inf')

    # 寻找匹配类型的充电桩
    for pile_id, queue in state.charging_piles.items():
        is_fast = pile_id in ['A', 'B']
        if (mode == "fast" and not is_fast) or (mode == "slow" and is_fast):
            continue
        if len(queue) >= state.CHARGING_QUEUE_LIMIT:
            continue

        wait_time = sum(car["request_power"] / (30 if is_fast else 7) for car in queue)
        self_time = vehicle["request_power"] / (30 if is_fast else 7)
        total_time = wait_time + self_time

        if total_time < min_time:
            best_pile = pile_id
            min_time = total_time

    if best_pile:
        state.charging_piles[best_pile].append(vehicle)
        return {
            "message": f"车辆 {vehicle['id']} 分配到充电桩 {best_pile}，预计总耗时 {round(min_time, 2)} 小时"
        }
    else:
        # 如果没有充电桩队列空位，则车辆回到等候区队尾
        state.waiting_area.insert(0, vehicle)
        return {"message": "暂无充电桩空位，继续等待"}

