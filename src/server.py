import queue
import threading

import uvicorn
from fastapi import FastAPI

from core import state_read
from core.charging_area import ChargingZone
from core.reporter import Reporter, FeeConfig
from core.virtual_time import time_factor, VirtualTime
from core.waiting_area import WaitingArea
from route import user, admin, system

app = FastAPI()
app.include_router(user.router, tags=["用户"])
app.include_router(admin.router, tags=["管理员"])
app.include_router(system.router, tags=["系统"])

# 等候区大小
waiting_zone_size = 6
# 充电速度，单位 度/小时
fast_speed = 30
slow_speed = 7
# 充电桩排队队列大小
wait_queue_length = 1
# 各类型充电桩数量
fast_num = 1
slow_num = 1
# 等候区与充电区通信的信号量
semaphore_f = threading.Semaphore(fast_num * (wait_queue_length + 1))
semaphore_t = threading.Semaphore(slow_num * (wait_queue_length + 1))
# 充电区交给等候区重新调度的故障/停止充电桩车辆
reschedule_t = queue.Queue()
reschedule_f = queue.Queue()
# 报告队列
report_queue = queue.Queue()
# 费率
PeakRate = 1.0
NormalRate = 0.7
OffPeakRate = 0.4
ServiceFeeRate = 0.8
@app.get("/")
async def root():
    return {"message": "hello world"}

if __name__ == '__main__':

    charging_zone = ChargingZone(fast_num, slow_num, semaphore_t, semaphore_f,
                                 report_queue,
                                 fast_speed, slow_speed,
                                 wait_queue_length)
    waiting_zone = WaitingArea(charging_zone, semaphore_t, semaphore_f, waiting_zone_size)
    reporter = Reporter(report_queue, time_factor, FeeConfig(PeakRate, NormalRate, OffPeakRate, ServiceFeeRate))
    vir = VirtualTime()
    # 依赖注入
    charging_zone.reschedule_t = reschedule_t
    charging_zone.reschedule_f = reschedule_f
    charging_zone.vir = vir
    waiting_zone.reschedule_t = reschedule_t
    waiting_zone.reschedule_f = reschedule_f
    reporter.vir = vir
    user.charging_zone = charging_zone
    user.waiting_zone = waiting_zone
    state_read.charging_zone = charging_zone
    state_read.waiting_zone = waiting_zone
    state_read.vir = vir
    admin.charging_area = charging_zone
    # 启动线程
    charging_zone.start()
    waiting_zone.start()
    reporter.start()
    vir.start()

    uvicorn.run(app="server:app", host="0.0.0.0", port=8080)
