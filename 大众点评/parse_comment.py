# -*- coding:utf-8 -*-

import re
from lxml import etree
from scrapy import Selector
from bs4 import BeautifulSoup
import requests

def parse_comment(comment, css_result, comment_dict):
    """
    解析评论页并提取数据
    """
    name = comment.xpath('.//a[@class="name"]/text()').extract_first().strip()
    # star = ' '.join(li.xpath('//span[@class="score"]//text()'))
    time = comment.xpath('.//span[@class="time"]/text()').extract_first().strip('\n\r \t')
    score = ' '.join(map(lambda s: s.strip('\n\r \t'), comment.xpath('.//span[@class="score"]//text()').extract()))
    # if comment.find('div', class_='review-words Hide'):
    if comment.css('div[class="review-words Hide"]'):
        comment = str(comment.css('div[class="review-words Hide"]').extract_first())
    else:
        comment = str(comment.css('.review-words').extract_first())
    comment = process_comment(comment, css_result, comment_dict)
    data = {
        'name': name,
        'comment': comment,
        'score': score,
        'time': time,
    }
    return data

def process_phone_number(fake_num):
    phone_number =''
    phone_number_dict = {
        '\uefeb': '1', '\ue4ff': '2', '\uf70d': '3', '\ue6ec': '4', '\uf404': '5', '\ue65d': '6', '\ue284': '7',
        '\uf810': '8', '\ue27b': '9', '\uec2d': '0'
    }
    for i in fake_num:
        if i in phone_number_dict.keys():
            phone_number += phone_number_dict[i]
        else:
            phone_number += i
    return phone_number

def svg_result(css_result):
    """
    解析svg链接，获取替换字典
    """
    svg_links = re.findall('.*?background-image: url\((.*?svgtextcss.*?.svg)\)', css_result)
    print(svg_links)
    # svg链接个数顺序都不固定，随时会变，根据上面的svg链接列表找到具体的评论字典链接
    # 目前svg链接有三个，分别是数字字典链接：处理电话号码；地址字典链接：处理地址；评论字典链接：处理评论
    # 通过将svg链接复制进浏览器观察，得知最大的字典及评论字典为列表第三个，所以列表索引为2
    svg_link = 'http:' + svg_links[2]
    print(svg_link)

    resp = requests.get(svg_link)
    # print(resp.text)
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, 'lxml')
    comment_dict = {}
    lis = soup.select('text')
    for li in lis:
        y = li['y']
        word = li.get_text()
        comment_dict[y] = word
    print(comment_dict)

    return comment_dict

def process_comment(comment, css_result, words_dict):
    if re.findall('<div class="review-words Hide">(.*)<div class="less-words">', comment, re.S):
        comment = re.findall('<div class="review-words Hide">(.*?)<div class="less-words">', comment, re.S)[0]
    if re.search('<img.*?>', comment):
        comment = re.sub('<img.*?>', '', comment)
    items = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', comment, re.S)
    for item in items:
        if item in css_result:
            # 获取x, y坐标
            x, y = re.search('\.%s{background:-(\d+).0px -(\d+).0px;}' % item, css_result, re.S).group(1, 2)
            # print(x, y)
            for number in list(words_dict.keys()):
                if int(y) > int(number):
                    continue
                else:
                    #line = words_dict[number]
                    str = words_dict[number]
                    offset = int(int(x) / 14) + 1
                    word = str[offset - 1]
                    comment = re.sub('<svgmtsi class="%s"></svgmtsi>' % item, word, comment)
                    comment = comment.replace('<br>', '')
                    break
            continue
    return comment.strip()