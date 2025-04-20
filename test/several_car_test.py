import requests

# 测试配置
BASE_URL = "http://127.0.0.1:8080/user/charge"
LOGIN_URL = "http://127.0.0.1:8080/user/login"
PARAMS_F = {"mode": "F", "power": 20}
PARAMS_T = {"mode": "T", "power": 20}
TOKENS_F = [

]
TOKENS_T = [
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjowLCJjYXJfaWQiOiJcdTY4NDJGRDQ0RUcyIiwiZXhwIjoxNzQ1MzgzNzExfQ.N7Pnd_pITp_KHPKG8TD7cH5DuR8pv7-eM9HRJuN-Ywg",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJjYXJfaWQiOiJcdTc0M2NCRlFHNzcwIiwiZXhwIjoxNzQ1MzgzNzExfQ.K3RWPxrVhelG6E3aJuQI_L-CPzdguxkEXTajY4nDfWQ",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJjYXJfaWQiOiJcdTZlNThIRjJFVTFaIiwiZXhwIjoxNzQ1MzgzNzExfQ.yDm-mz9htpofEX4qOOxXCX78xXM7-cu_KLaZ3vHQMKo",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJjYXJfaWQiOiJcdTljODFURlBYWURLIiwiZXhwIjoxNzQ1MzgzNzExfQ._dBD_5GgFaKdypmPK0LYzslkZEswmO6fIhD31bU4HxM",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJjYXJfaWQiOiJcdTc2OTZMRkhUVTI0IiwiZXhwIjoxNzQ1MzgzNzExfQ.xvijAIa_sJRIK5Yq4wIejxPpoOAGDDLSF8mu7sSLsZo",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1LCJjYXJfaWQiOiJcdThjNmJIRlRDRFFHIiwiZXhwIjoxNzQ1MzgzNzExfQ.T8LFYIpo9-7b3eOuFc-ClZpsxo5nlsZv4j8IVriA1Ak",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJjYXJfaWQiOiJcdTgyY2ZEREtVM0syIiwiZXhwIjoxNzQ1MzgzNzExfQ.qgdS7R4yftEySgi3HTVpMi0XvCXd08HHJtQI-H5sedk",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJjYXJfaWQiOiJcdThjNmJGRjBFWjlOIiwiZXhwIjoxNzQ1MzgzNzExfQ.GhwdjVk0W9-6VUYD7BqdQeQ1rWxBFqwdB9Q9Kt2JxJU",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4LCJjYXJfaWQiOiJcdTZlMWRDRlVHRDAwIiwiZXhwIjoxNzQ1MzgzNzExfQ.rn04pMYWyQkuMmo1Nh75FgxSj_r4YJTzagF0-f2MNHk",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJjYXJfaWQiOiJcdTZkNTlYRDBTMkU4IiwiZXhwIjoxNzQ1MzgzNzExfQ.aAkSGs8CkFSSplSuTOMXjVwA77vl2uRle2OmyGq2yF4",

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
