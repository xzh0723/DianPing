# -*- coding:utf-8 -*-

import requests
from config import *


def get_random_proxy():
    """
    穷逼学生只能用崔大的免费代理池框架，但是爬来的代理质量确实差，根本不能用来爬大众点评
    """
    try:
        response = requests.get(PROXY_URL)
        if response.status_code == 200:
            proxy = response.text
            print('使用代理:', proxy)
            return proxy
    except requests.ConnectionError:
        return False