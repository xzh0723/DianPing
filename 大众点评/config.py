# -*- coding:utf-8 -*-

import random

MAX_PAGES = 20

UA_LIST=[
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0"
    ]

with open('./ua.log', 'r', encoding='utf-8') as f:
    random_ua = random.choice(f.read().split('\n'))

HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN',
            'Cache-Control': 'no-cache',
            'Connection': 'Keep-Alive',
            'Host': 'www.dianping.com',
            'Referer': 'http://www.dianping.com/chengdu/ch10/g110',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random_ua,
            'Cookie': 'cy=344; cye=changsha; _lxsdk_cuid=16ad513ed49c8-0e37f14e5c0548-11656d4a-100200-16ad513ed4a64; _lxsdk=16ad513ed49c8-0e37f14e5c0548-11656d4a-100200-16ad513ed4a64; _hc.v=6bda69c2-e301-f0f1-b2e9-0986a246812a.1558353014; s_ViewType=10; ua=dpuser_7476989533; ctu=67c5009b0aff4cb1bcd00edead94f17f36fe58ee588f2952ab3af3c60353063c; _lxsdk_s=16ada252821-b64-328-84%7C1524916518%7C127; _lx_utm=utm_source%3Dso.com%26utm_medium%3Dorganic'
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            # "Proxy-Tunnel": str(random.randint(1,10000))  # 使用亿牛云代理时需设置
}

PROXY_URL = 'http://localhost:5555/random'

MONGO_URI = 'localhost'
MONGO_PORT = 27017

DEFAULT_STAR = '三星级商户'
DEFAULT_NAME = 'Unnamed'
DEFAULT_NUM = 10
