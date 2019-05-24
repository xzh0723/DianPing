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
            'Cookie': 'cy=344; cye=changsha; _lxsdk_cuid=16ae491f14ec8-0b15bbe4294f4e-7a1b34-100200-16ae491f14ec8; _lxsdk=16ae491f14ec8-0b15bbe4294f4e-7a1b34-100200-16ae491f14ec8; _hc.v=086b8d48-9c22-24d8-6ea7-27d6082e5eae.1558612931; dper=9334aedd67a8f58a39212bb877648c4d4d3ad826e9984d0b3c1dde28095f25f9aecc6122726aac6acf7dfb1290f546ee9faf1b0edc8d778c6905fd8c8bd30bb35dab8b0f4f77633f5a2ce3c3c14ef020f2143b5a0f7760a9877d272f4a0fd40c; ua=dpuser_1882149410; ctu=afb940fdd57f6cf8407de823acf54cbe6399c58009af3730aad8f3d47c980b80; s_ViewType=10; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3Dso.com%26utm_medium%3Dorganic; _lxsdk_s=16ae88e2730-c16-262-abe%7C%7C36'
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            # "Proxy-Tunnel": str(random.randint(1,10000))  # 使用亿牛云代理时需设置
}

PROXY_URL = 'http://localhost:5555/random'

MONGO_URI = 'localhost'
MONGO_PORT = 27017

DEFAULT_STAR = '三星级商户'
DEFAULT_NAME = 'Unnamed'
DEFAULT_NUM = 10
