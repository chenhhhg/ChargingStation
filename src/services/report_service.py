from core import state
from collections import defaultdict

def get_report():
    stats = defaultdict(lambda: {
        "count": 0,
        "total_power": 0,
        "total_time": 0,
        "avg_time": 0
    })

    for record in state.charging_records:
        pile = record["pile_id"]
        stats[pile]["count"] += 1
        stats[pile]["total_power"] += record["power"]
        stats[pile]["total_time"] += record["time"]

    # 计算平均时间
    for pile_id in stats:
        count = stats[pile_id]["count"]
        if count > 0:
            stats[pile_id]["avg_time"] = round(stats[pile_id]["total_time"] / count, 2)

    return stats
