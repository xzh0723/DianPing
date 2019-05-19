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
            'Cookie': 'll=7fd06e815b796be3df069dec7836c3df; uamo=18829040039; _hc.v=8cce09d3-26bc-3063-0e21-5fa782bf407b.1558225212; ctu=67c5009b0aff4cb1bcd00edead94f17f70ec0cfe09559a18070d3d6b0a118781; dper=99c02fd71e25712ab1ae8ccb26169262738071c10020ae7c1c6457b41978f18dfd442181c079fb47e7b84a32effd6c80d6bb0fe7a2a338939e9e6972db1254ff548f8d5c8805272733da64ae37c1e9413f45103edfde39cc9da0772eaf2e0a12; _lxsdk_cuid=16acd75d18f87-0e785115adc4cd-784a5037-100200-16acd75d190c8; s_ViewType=10; _lxsdk=16acd75d18f87-0e785115adc4cd-784a5037-100200-16acd75d190c8; ua=dpuser_7476989533; _lx_utm=utm_source%3Dso.com%26utm_medium%3Dorganic; cye=chengdu; lgtoken=0841aadf7-b04d-41bb-b7cb-98469f423726; _lxsdk_s=16acd75d192-be-019-e4f%7C%7C133; cy=8; _dp.ac.v=fad4b29d-2e5f-4347-a848-3949c478b96a'
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            # "Proxy-Tunnel": str(random.randint(1,10000))  # 使用亿牛云代理时需设置
}


DEFAULT_STAR = '三星级商户'
DEFAULT_NAME = 'Unnamed'
DEFAULT_NUM = 10
