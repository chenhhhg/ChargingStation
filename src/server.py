import threading

import uvicorn
from fastapi import FastAPI
from route import user, admin, report, fault, state
from core import virtual_time
from core.scheduler import time_loop
from services.waiting_service import wait_schedule
from services.charging_service import charge_loop

app = FastAPI()
# 注册路由
app.include_router(user.router, tags=["鉴权"])
app.include_router(admin.router, tags=["鉴权"])
app.include_router(fault.router, prefix="/fault", tags=["故障处理"])
app.include_router(virtual_time.router, prefix="/time", tags=["虚拟时间"])
app.include_router(state.router, prefix="/state", tags=["系统状态"])
app.include_router(report.router, prefix="/report", tags=["报表"])

# 启动线程
threading.Thread(target=time_loop, daemon=True).start()
threading.Thread(target=wait_schedule, daemon=True).start()
threading.Thread(target=charge_loop, daemon=True).start()


@app.get("/")
async def root():
    return {"message": "hello world"}

if __name__ == '__main__':
    uvicorn.run(app="server:app", host="0.0.0.0", port=8080)
