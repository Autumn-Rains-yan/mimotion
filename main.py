import os
import requests
import traceback
import random
import json
from datetime import datetime
import math
import time


headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://d.faithxy.com',
    'Pragma': 'no-cache',
    'Referer': 'https://d.faithxy.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

def desensitize_user_name(user):
    if len(user) <= 8:
        ln = max(math.floor(len(user) / 3), 1)
        return f'{user[:ln]}***{user[-ln:]}'
    return f'{user[:3]}****{user[-4:]}'


def make_request(user, pwd, num):
    payload = {
        'phone': user,
        'pwd': pwd,
        'num': str(num)
    }
    response = requests.post('https://d.faithxy.com/motion/api/motion/Xiaomi', headers=headers, data=payload)
    response_data = response.json()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    desensitized_user = desensitize_user_name(user)
    if response_data.get("code") == 200:
        print(f'[{current_time}]\n账号{desensitized_user}执行成功\n随机步数为{str(num)}')
    else:
        print(f'[{current_time}]\n账号{desensitized_user}执行失败')


if __name__ == "__main__":
    if os.environ.__contains__("CONFIG") is False:
        print("未配置CONFIG变量，无法执行")
        exit(1)
    else:
        # region 初始化参数
        config = dict()
        try:
            config = dict(json.loads(os.environ.get("CONFIG")))
        except:
            print("CONFIG格式不正确，请检查Secret配置，请严格按照JSON格式：使用双引号包裹字段和值，逗号不能多也不能少")
            traceback.print_exc()
            exit(1)
        users = config["USER"].split('#')
        passwords = config["PWD"].split('#')
        rangeNum = 0
        sleepNum = int(config["SLEEP_GAP"])
        for user, pwd in zip(users, passwords):
            if rangeNum != 0:
                print(f'请等待{sleepNum}秒')
                time.sleep(sleepNum)
            rangeNum += 1
            num = random.randint(int(config["MIN_STEP"]), int(config["MAX_STEP"]))
            make_request(user, pwd, num)



