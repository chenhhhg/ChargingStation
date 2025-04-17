import queue
import threading

import uvicorn
from fastapi import FastAPI
from core.virtual_time import time_factor, VirtualTime
from route import user, admin, system
from core import state_read
from core.charging_area import ChargingZone
from core.waiting_area import WaitingArea
from core.reporter import Reporter, FeeConfig
app = FastAPI()
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(system.router)

# 充电速度，单位 度/小时
fast_speed = 30
slow_speed = 7
# 充电桩排队队列大小
wait_queue_length = 2
# 各类型充电桩数量
fast_num = 2
slow_num = 3
# 等候区与充电区通信的信号量
semaphore_f = threading.Semaphore(fast_num * wait_queue_length + 1)
semaphore_t = threading.Semaphore(slow_num * wait_queue_length + 1)
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
    waiting_zone = WaitingArea(charging_zone, semaphore_t, semaphore_f)
    reporter = Reporter(report_queue, time_factor, FeeConfig(PeakRate, NormalRate, OffPeakRate, ServiceFeeRate))
    vir = VirtualTime()
    charging_zone.vir = vir
    # 启动线程
    charging_zone.start()
    waiting_zone.start()
    reporter.start()
    vir.start()
    # 依赖注入
    user.charging_zone = charging_zone
    user.waiting_zone = waiting_zone
    state_read.charging_zone = charging_zone
    state_read.waiting_zone = waiting_zone
    state_read.vir=vir

    uvicorn.run(app="server:app", host="0.0.0.0", port=8080)
