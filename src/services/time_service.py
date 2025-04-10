virtual_time = {
    "current": 0,
    "factor": 1.0
}

def get_virtual_time():
    return virtual_time

def update_virtual_time(factor: float):
    virtual_time["factor"] = factor
    return {"message": f"已设置倍速为 {factor}x"}
