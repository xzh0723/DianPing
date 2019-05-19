# -*- coding:utf-8 -*-

import requests
from config import *


def get_random_proxy():
    try:
        response = requests.get(PROXY_URL)
        if response.status_code == 200:
            proxy = response.text
            print('使用代理:', proxy)
            return proxy
    except requests.ConnectionError:
        return False