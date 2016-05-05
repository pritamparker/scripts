#!/usr/bin/env python3

import argparse
import requests

from colorama import Fore, init

URL = "https://www.safaribooksonline.com"

cookies = {
    'BrowserCookie': 'f8df5be6-a3ba-43b0-b803-260273eac31e',
    'liveagent_ptid': '713515c5-7550-43fb-b210-40593eefc7a5',
    'liveagent_sid': '4b5cec4a-98a9-413d-9c23-ff02a2e795ed',
    'csrfsafari': 'tvwBTf1m4Uocs8ZEBz6OW0dUSTkZdSiK',
    'corp_sessionid': '67wr9jxg5fioc7krvc89icn5svrpl75x',
}

headers = {
    'Origin': 'https://www.safaribooksonline.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.safaribooksonline.com/',
}

data = 'csrfmiddlewaretoken=&csrfmiddlewaretoken=tvwBTf1m4Uocs8ZEBz6OW0dUSTkZdSiK&email=glitstreet2&password1=qsxfthnko2&is_login_form=true&leaveblank=&dontchange=http%3A%2F%2F'

r = requests.post(URL+'/accounts/login/', headers=headers, cookies=cookies, data=data)
