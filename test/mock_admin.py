from os import remove

import requests
import time
import json

url = "http://localhost:8080/admin/"
sub = ["users","bills","piles"]
while True:
    time.sleep(1)
    try:
        for _, s in enumerate(sub):
            # 发送GET请求并获取响应
            response = requests.get(url + s)
            response.raise_for_status()  # 检查HTTP错误

            # 解析响应内容为JSON并格式化
            data = response.json()
            formatted_data = json.dumps(data, indent=10, ensure_ascii=False)
            print(f"以下为 {s}")
            print(formatted_data)

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except json.JSONDecodeError:
        print("响应内容不是有效的JSON")

