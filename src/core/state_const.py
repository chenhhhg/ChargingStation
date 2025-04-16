from enum import Enum

class VehicleStatus(Enum):
    """车辆状态枚举类"""
    LOGGED_IN = "已登录"                # 车辆已接入系统但未进入调度流程
    WAITING = "等候中"                 # 在等待区等待分配充电桩
    QUEUED = "排队中"                  # 已分配到充电桩的等待队列
    CHARGING = "充电中"                # 正在充电状态
    PENDING_RESCHEDULE = "等待重新调度"  # 充电失败需要重新调度

# 使用示例
if __name__ == "__main__":
    # 获取所有状态
    print([status.value for status in VehicleStatus])
    # 状态转换示例
    current_status = VehicleStatus.WAITING
    print(f"当前状态: {current_status.value}")
