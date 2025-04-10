from fastapi import FastAPI
from routers import fault, waiting_area, charging_area, virtual_time, state
from core.scheduler import time_loop
from routers import report
import threading

app = FastAPI()

# 注册路由
app.include_router(fault.router, prefix="/fault", tags=["故障处理"])
app.include_router(waiting_area.router, prefix="/waiting", tags=["等候区"])
app.include_router(charging_area.router, prefix="/charging", tags=["充电区"])
app.include_router(virtual_time.router, prefix="/time", tags=["虚拟时间"])
app.include_router(state.router, prefix="/state", tags=["系统状态"])
app.include_router(report.router, prefix="/report", tags=["报表"])

# 启动时间线程
threading.Thread(target=time_loop, daemon=True).start()
