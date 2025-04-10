from core import state

def handle_fault(pile_id: str):
    if pile_id not in state.charging_piles:
        return {"error": f"充电桩 {pile_id} 不存在"}

    queue = state.charging_piles[pile_id]
    released_vehicles = []

    while queue:
        car = queue.pop(0)
        released_vehicles.append(car["id"])

        # 若等候区未满，重新加入等候区
        if len(state.waiting_area) < state.WAITING_LIMIT:
            state.waiting_area.append({
                "id": car["id"],
                "mode": "fast" if pile_id in ['A', 'B'] else "slow",
                "request_power": car["request_power"]
            })

    return {
        "message": f"已处理充电桩 {pile_id} 故障，释放车辆 {released_vehicles}"
    }
