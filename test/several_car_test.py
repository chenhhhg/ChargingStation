import requests

# 测试配置
BASE_URL = "http://127.0.0.1:8080/user/charge"
LOGIN_URL = "http://127.0.0.1:8080/user/login"
PARAMS_F = {"mode": "F", "power": 20}
PARAMS_T = {"mode": "T", "power": 20}
TOKENS_F = [

]
TOKENS_T = [
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjowLCJjYXJfaWQiOiJcdTY2NGJaRFRLUUMxIiwiZXhwIjoxNzQ2NTI5MDg3fQ.iaoBW1fuLQgE_Z67WuKex-u0xIjRXVNcUeHQBgAkNwQ",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJjYXJfaWQiOiJcdTRlYWNCRjk3WjRWIiwiZXhwIjoxNzQ2NTI5MDg3fQ._sMVGAtDczRPtXhjgkAI_XdVXs_GXT1rRCPiHFiunI0",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJjYXJfaWQiOiJcdTRlYWNYREFTSk02IiwiZXhwIjoxNzQ2NTI5MDg3fQ.VklmJO1CsxN6ll9ruhLMhsCPt8OK2mEgRucrBTL_UdQ",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJjYXJfaWQiOiJcdThkMzVIRlNaWkdMIiwiZXhwIjoxNzQ2NTI5MDg3fQ.K6wKSEjnX49wKG_dCtgJdBqxld8NkQBGCz6A362QoQE",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJjYXJfaWQiOiJcdTgyY2ZVREpVTE1DIiwiZXhwIjoxNzQ2NTI5MDg3fQ.bNwLZux3CfixJ4_KeaAQo5GlyJlB35W38eUljWEY5C8",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1LCJjYXJfaWQiOiJcdTc2OTZHRFBFWU44IiwiZXhwIjoxNzQ2NTI5MDg3fQ.qdigBqS1JNinYjpn3igVIP8CfGEIsfGoeRmf2qYI5xo",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJjYXJfaWQiOiJcdTRlYWNORjhWVEdEIiwiZXhwIjoxNzQ2NTI5MDg3fQ.55jVzK0L0V4LkxEya5aqkDGjVWzylPVdiHk-rj5Utdw",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJjYXJfaWQiOiJcdTkxMDJWRFhFWEtRIiwiZXhwIjoxNzQ2NTI5MDg3fQ.ACP8rnGj1auHWGnvwze8c28qR3KK6Y7G0f4Y9RF8vh8",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4LCJjYXJfaWQiOiJcdTkxMDJURFhGQ1oxIiwiZXhwIjoxNzQ2NTI5MDg3fQ.JJOUu9Mq2yYetOoZeeFQCTZx-_tEtoTpFO85NE1pCC4",
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJjYXJfaWQiOiJcdTc0M2NLRjlFVVVVIiwiZXhwIjoxNzQ2NTI5MDg3fQ.hFuAFlZ5iTJaG6FAc2fZWCb5ZXeuZQkOCLpne1-BXVQ",

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
