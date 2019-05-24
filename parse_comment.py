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

def process_cnum(number, css_result, num_dict):
    """
    处理数字
    """
    items = re.findall('<cc class="(.*?)"></cc>', number, re.S)
    number = re.sub('</b>', '', re.sub('<b>', '', number))
    for item in items:
        if item in css_result:
            x, y = re.search('\.%s{background:-(\d+).0px -(\d+).0px;}' % item, css_result, re.S).group(1, 2)
            # print(x, y)
            for num in list(num_dict.keys()):
                if int(y) > int(num):
                    continue
                else:
                    offset = int(int(x) / 14) + 1
                    str = num_dict[num]
                    real_num = str[offset - 1]
                    number = re.sub('<cc class="%s"></cc>' % item, real_num, number)
    return number

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

def process_caddress(address, css_result, address_dict):
    """
    处理地址信息
    """
    address = address.replace('<span class="addr">', '').replace('</span>', '')
    items = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', address, re.S)
    for item in items:
        if item in css_result:
            # 获取x, y坐标
            x, y = re.search('\.%s{background:-(\d+).0px -(\d+).0px;}' % item, css_result, re.S).group(1, 2)
            # print(x, y)
            for num in list(address_dict.keys()):
                if int(y) > int(num):
                    continue
                else:
                    offset = int(int(x) / 14) + 1
                    #print('{}所在行第{}列'.format(num, offset))
                    str = address_dict[num]
                    word = str[offset - 1]
                    address = re.sub('<svgmtsi class="%s"></svgmtsi>' % item, word, address)
                    break
            continue
    return address

def process_comment(comment, css_result, words_dict):
    # 判断是否评论过长，有Hide属性则需要展开
    if re.findall('<div class="review-words Hide">(.*)<div class="less-words">', comment, re.S):
        comment = re.findall('<div class="review-words Hide">(.*?)<div class="less-words">', comment, re.S)[0]
    if re.findall('div class="review-words">(.*)</div>', comment, re.S):
        comment = re.findall('div class="review-words">(.*)</div>', comment, re.S)[0]
    # 判断是否有图片，若有则剔除，只留下纯文本
    if re.search('<img.*?>', comment):
        comment = re.sub('<img.*?>', '', comment)
    items = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', comment, re.S)
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

def svg_result(css_result):
    """
    解析svg链接，获取替换字典
    """
    svg_links = re.findall('.*?background-image: url\((.*?svgtextcss.*?.svg)\)', css_result)
    print(svg_links)
    # svg链接个数顺序都不固定，随时会变，根据上面的svg链接列表找到具体的评论字典链接
    # 目前svg链接有三个，分别是数字字典链接：处理电话号码；地址字典链接：处理地址；评论字典链接：处理评论
    # 通过将svg链接复制进浏览器观察，根据具体情况改变index索引顺序
    address_dict = {}
    comment_dict = {}
    num_dict = {}
    for index, svg_link in enumerate(svg_links):
        svg_link = 'http:' + svg_link
        print(svg_link)
        response = requests.get(svg_link)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        # 如果你获取的svg文件有三个，那么说明数字也是svg矢量图替换，请将下面的注释去掉，将第二个index改成==1，获取num_dict并返回
        # 还有就是数字、地址和标签的三个svg文件的位置会动态变化，可根据svg链接列表的具体顺序自行调整
        if index == 0:
            # 地址
            items = soup.find_all('text')
            for item in items:
                y = item['y']
                word = item.get_text()
                address_dict[y] = word
            print(address_dict)
        elif index == 2:
            # 评论
            items = soup.select('text')
            for item in items:
                y = item['y']
                word = item.get_text()
                comment_dict[y] = word
            print(comment_dict)
        else:
            # 数字
            nums = soup.select('text')
            for num in nums:
                # print(num)
                y = num['y']
                num = num.get_text()
                num_dict[y] = num
            print(num_dict)

    return num_dict, address_dict, comment_dict