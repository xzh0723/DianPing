# -*- coding:utf-8 -*-

import re
from lxml import etree
from bs4 import BeautifulSoup
from config import *
import requests

def parse_comment(html):
    """
    解析评论页并提取数据
    """
    html = etree.HTML(html)
    phone_info = html.xpath('//div[@class="phone-info"]//text()')
    phone_number = process_phone_number(phone_info)
    # print(phone_number.strip())

    css_link = 'http:' + re.findall('.*?href="(.*?.svgtextcss.*?)"', html)[0]
    # print(css_link)
    resp = requests.get(css_link)
    # print(resp.text)
    css_result = resp.text

    line_dict, comment_dict = svg_result(css_result)

    for li in html.xpath('//*[@class="reviews-items"]/ul/li'):
        name = li.xpath('//a[@class="name"]/text()').strip()
        #star = ' '.join(li.xpath('//span[@class="score"]//text()'))
        time = li.xpath('.//span[@class="time"]/text()')[0].strip('\n\r \t')
        score = '/'.join(map(lambda s: s.strip('\n\r \t'), li.xpath('.//span[@class="score"]//text()')))
        comment = ''.join(li.xpath('.//div[@class="review-words Hide"]/text()')).strip('\n\r \t')
        if not comment:
            comment = ''.join(li.xpath('.//div[@class="review-words"]/text()')).strip('\n\r \t')
        comment = process_comment(comment, css_result, line_dict, comment_dict)
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
    svg_link = 'http:' + re.findall('.*?background-image: url\((.*?svgtextcss.*?.svg)\)', css_result)[0]
    print(svg_link)

    comment_dict = {}
    line_dict = {}
    resp = requests.get(svg_link)
    # print(resp.text)
    resp.encoding = resp.apparent_encoding
    # Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration
    # 以上报错，将res.text 改为 res.content即可
    soup = BeautifulSoup(resp.text, 'lxml')
    paths = soup.find_all('path')
    for path in paths:
        id_ = path['id']
        number = path['d'].split(' ')[1]
        line_dict[number] = id_
    print(line_dict)

    # soup_1 = BeautifulSoup(resp.text, 'lxml')
    # 大众点评真的心机，太阴险了，这里的这个节点textpath，源码里标的是textPath，然后我死活匹配不出来，折腾了老半天，也怪我自己没有仔细看打印的内容。。
    lines = soup.find_all('textpath')
    # lines = re.findall('xlink:href="#(\d+).*?>(.*?)</textPath>', res.text, re.S)
    # print(lines)
    for line in lines:
        # print(line)
        # num = line.group(1)
        # content = line.group(2)
        num = line['xlink:href'].replace('#', '')
        content = line.get_text()
        # print(content)
        comment_dict[num] = content
    print(comment_dict)

    return line_dict, comment_dict

def process_comment(comment, css_result, line_dict, comment_dict):
    tags = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', comment, re.S)
    for tag in tags:
        if tag in css_result:
            # 获取x, y坐标
            x, y = re.search('\.%s{background:-(\d+).0px -(\d+).0px;}' % tag, css_result, re.S).group(1, 2)
            # print(x, y)
            for number in list(line_dict.keys()):
                if int(y) > int(number):
                    continue
                else:
                    line = line_dict[number]
                    str = comment_dict[line]
                    offset = int(int(x) / 14) + 1
                    word = str[offset - 1]
                    comment = re.sub('<svgmtsi class="%s"></svgmtsi>' % tag, word, comment)
                    break
            continue
    # print(comment)
    return comment