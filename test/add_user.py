from os import remove

import requests
import time
import json

url = "http://localhost:8080/admin/test/add/user"
# 发送GET请求并获取响应
response = requests.post(url)

