import threading
import time
from core import state
from services import charging_service

# 自动推进虚拟时间并触发充电处理
def time_loop(interval_sec=10):
    while True:
        time.sleep(interval_sec)

        # 时间 +1 小时
        state.virtual_time["now"] += 1

        # 自动调用充电逻辑
        charging_service.process_charging_queue()

        print(f"[模拟时间] 虚拟时间已推进至 {state.virtual_time['now']} 小时")
