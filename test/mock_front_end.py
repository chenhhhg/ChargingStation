import time

import requests

if __name__ == '__main__':
    while True:
        time.sleep(0.5)
        print(requests.get(url="http://localhost:8080/system/global").text)