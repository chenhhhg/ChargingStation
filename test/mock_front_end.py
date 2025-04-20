from os import remove
import atexit
import requests
import time
import json

url = "http://localhost:8080/system/global"
try:
    remove("./output.json")
except Exception:
    pass
with open("./output.json", "a", encoding="utf-8") as f:
    f.write("[")
def f():
    with open("./output.json", "a", encoding="utf-8") as f:
        f.write("]")
atexit.register(f)
while True:
    time.sleep(0.5)
    try:
        # 发送GET请求并获取响应
        response = requests.get(url)
        response.raise_for_status()  # 检查HTTP错误

        # 解析响应内容为JSON并格式化
        data = response.json()
        formatted_data = json.dumps(data, indent=10, ensure_ascii=False)

        # 将格式化后的JSON写入文件
        with open("./output.json", "a", encoding="utf-8") as f:
            f.write(formatted_data)
            f.write(",\n")

        print("数据已更新到output.json")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except json.JSONDecodeError:
        print("响应内容不是有效的JSON")

