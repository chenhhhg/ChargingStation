import threading

import uvicorn
from fastapi import FastAPI
from route import user, admin, system
from core import state_read
from core.charging_area import ChargingZone
from core.waiting_area import WaitingArea


app = FastAPI()
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(system.router)

pile_num = 2
fast_rate = 0.5
fast_speed = 30
slow_speed = 5
wait_queue_length = 1
semaphore = threading.Semaphore(pile_num * wait_queue_length)

@app.get("/")
async def root():
    return {"message": "hello world"}

if __name__ == '__main__':# 初始化充电区（3个桩）

    charging_zone = ChargingZone(pile_num, semaphore, fast_rate, fast_speed, slow_speed, wait_queue_length)
    # 依赖注入
    waiting_zone = WaitingArea(charging_zone, semaphore)

    # 启动线程
    charging_zone.start()
    waiting_zone.start()

    # 依赖注入
    user.charging_zone = charging_zone
    user.waiting_zone = waiting_zone
    state_read.charging_zone = charging_zone
    state_read.waiting_zone = waiting_zone

    uvicorn.run(app="server:app", host="0.0.0.0", port=8080)
