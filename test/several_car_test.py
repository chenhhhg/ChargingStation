import requests

# 测试配置
BASE_URL = "http://localhost:8080/user/charge"
PARAMS_F = {"mode": "F", "power": 120}
PARAMS_T = {"mode": "T", "power": 120}
TOKENS_F = [
]
TOKENS_T = [
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjowLCJjYXJfaWQiOiJcdTVkZGRVRjc3WTRYIiwiZXhwIjoxNzQ1MDU0NjkwfQ.-rYRq8tCEZzNE07Pmo2Xc9Z2vani7T7RQsS9tU2V-xc",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJjYXJfaWQiOiJcdTljODFIRlk1NVBKIiwiZXhwIjoxNzQ1MDU0NjkwfQ.cPCzRECsHkzXYtDTKzBTWvRSs8ddoy60ASYgHUc37IM",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJjYXJfaWQiOiJcdTllZDFHRFdORVdNIiwiZXhwIjoxNzQ1MDU0NjkwfQ.a10k4AIFIIgryibrTZlsjf07Doupwh5IC6NgIPALVEc",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJjYXJfaWQiOiJcdTg0OTlBRDZTRk1RIiwiZXhwIjoxNzQ1MDU0NjkwfQ.hvC1UyP_5J3C5rCDQPEyYmz2KdvL_R_SiSfj5NVNQK0",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4LCJjYXJfaWQiOiJcdTY4NDJERlVBVVYxIiwiZXhwIjoxNzQ1MDU0NjkwfQ.i4kiqAV8PQLawcqzqBf3S7vqdWn7U-LVjs-sOHc8Bdw",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJjYXJfaWQiOiJcdTUxODBORDBLSDZCIiwiZXhwIjoxNzQ1MDU0NjkwfQ.dS414vqlUp0t2RYBa0CjDVmk7fKazJeN0RrT6mwZxqw"
]

def send_request(single_token, mode):
    """发送单个请求"""
    headers = {"Authorization": single_token}

    try:
        # 使用 POST 方法（根据接口需求可改为 GET）
        response = requests.post(
            BASE_URL,
            params=PARAMS_F if mode == 0 else PARAMS_T,  # 参数放在 URL 查询字符串
            headers=headers,
            timeout=5
        )

        # 打印简略结果
        print(f"用户 {single_token.split('.')[1][:10]}... | 状态码: {response.status_code} | 响应: {response.text[:50]}...")

    except Exception as e:
        print(f"请求失败: {str(e)}")



if __name__ == "__main__":
    print("=== 开始发送测试请求 ===")
    for token in TOKENS_F:
        send_request(token, 0)
    for token in TOKENS_T:
        send_request(token, 1)
    print("=== 所有请求发送完成 ===")
