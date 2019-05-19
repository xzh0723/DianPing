# -*- coding:utf-8 -*-

import re
from lxml import etree
from bs4 import BeautifulSoup
from config import *
import requests

def parse_info(shop, css_result, num_dict, address_list, tag_dict):
    """
    解析数据
    """
    data = dict()
    # 店铺名称
    data['shop_name'] = shop.select('.tit a h4')[0].get_text()
    # 店铺封面
    data['img'] = shop.select('.pic a img')[0]['src']
    # 店铺链接
    data['src'] = shop.select('.tit a')[0]['href']
    # 星级
    data['star'] = shop.select('.comment')[0].find('span')['title']
    # 评论数
    comment_num = str(shop.select('.review-num b')[0])
    data['comment_num'] = process_num(comment_num, css_result, num_dict)
    # 人均价
    average_cost = str(shop.select('.mean-price b')[0])
    data['average_cost'] = process_num(average_cost, css_result, num_dict)
    # 口味
    sanitation_score = str(shop.select('.comment-list span:nth-child(1) b')[0])
    data['sanitation_score'] = process_num(sanitation_score, css_result, num_dict)
    # 环境
    environment_score = str(shop.select('.comment-list span:nth-child(2) b')[0])
    data['environment_score'] = process_num(environment_score, css_result, num_dict)
    # 服务
    service_score = str(shop.select('.comment-list span:nth-child(3) b')[0])
    data['service_score'] = process_num(service_score, css_result, num_dict)
    # 推荐菜
    data['recommend'] = shop.select('.recommend')[0].get_text().replace('\n', ' ')
    # 标签
    tag = str(shop.select('.tag-addr a:nth-child(1) .tag')[0])
    data['tag'] = process_tag(tag, css_result, tag_dict)
    # 地址
    xaddress = str(shop.select('.addr')[0])
    data['address'] = process_address(xaddress, css_result, address_list)
    return data

def parse_comment(html):
    """
    解析评论页并提取数据
    """
    phone_number_dict = {
        '\uefeb': '1', '\ue4ff': '2', '\uf70d': '3', '\ue6ec': '4', '\uf404': '5', '\ue65d': '6', '\ue284': '7',
        '\uf810': '8', '\ue27b': '9', '\uec2d': '0'
    }
    html = etree.HTML(html)
    phone_number = ''
    phone_info = html.xpath('//div[@class="phone-info"]//text()')
    for i in phone_info:
        if i in phone_number_dict.keys():
            phone_number += phone_number_dict[i]
        else:
            phone_number += i
    #print(phone_number.strip())
    for li in html.xpath('//*[@class="reviews-items"]/ul/li'):
        name = li.xpath('//a[@class="name"]/text()').strip()
        #star = ' '.join(li.xpath('//span[@class="score"]//text()'))
        time = li.xpath('.//span[@class="time"]/text()')[0].strip('\n\r \t')
        score = '/'.join(map(lambda s: s.strip('\n\r \t'), li.xpath('.//span[@class="score"]//text()')))
        comment = ''.join(li.xpath('.//div[@class="review-words Hide"]/text()')).strip('\n\r \t')
        if not comment:
            comment = ''.join(li.xpath('.//div[@class="review-words"]/text()')).strip('\n\r \t')
        data = {
            'name': name,
            'comment': comment,
            'score': score,
            'time': time,
        }
        return data

def process_num(process_num, css_result, num_dict):
    """
    处理数字
    """
    tags = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', process_num, re.S)
    process_num = re.sub('</b>', '', re.sub('<b>', '', process_num))
    for tag in tags:
        if tag in css_result:
            # 获取x, y坐标
            x, y = re.search('\.%s{background:-(\d+).0px -(\d+).0px;}' % tag, css_result, re.S).group(1, 2)
            #print(x, y)
            if int(y) <= int(list(num_dict.keys())[0]):
                offset = int((int(x) + 5) / 12)
                #print('第{}行第{}列'.format(1, offset))
                str = list(num_dict.values())[0]
                num = str[offset - 1]
                #print(num)
                process_num = re.sub('<svgmtsi class="%s"></svgmtsi>' % tag, num, process_num)
            elif int(y) <= int(list(num_dict.keys())[1]):
                offset = int((int(x) + 5) / 12)
                #print('第{}行第{}列'.format(2, offset))
                str = list(num_dict.values())[1]
                num = str[offset - 1]
                #print(num)
                process_num = re.sub('<svgmtsi class="%s"></svgmtsi>' % tag, num, process_num)
            else:
                offset = int((int(x) + 5) / 12)
                #print('第{}行第{}列'.format(3, offset))
                str = list(num_dict.values())[2]
                num = str[offset - 1]
                #print(num)
                process_num = re.sub('<svgmtsi class="%s"></svgmtsi>' % tag, num, process_num)
    return process_num

def process_address(address, css_result, address_list):
    """
    处理地址
    :param address:
    :param css_result:
    :param address_list:
    :return:
    """
    address = address.replace('<span class="addr">', '').replace('</span>', '')
    tags = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', address, re.S)
    for tag in tags:
        if tag in css_result:
            # 获取x, y坐标
            x, y = re.search('\.%s{background:-(\d+).0px -(\d+).0px;}' % tag, css_result, re.S).group(1, 2)
            #print(x, y)
            line = round((int(y) + 30) / 41)
            offset = int(int(x) / 12) + 1
            #print('第{}行第{}列'.format(line, offset))
            str = address_list[line - 1]
            word = str[offset - 1]
            address = re.sub('<svgmtsi class="%s"></svgmtsi>' % tag, word, address)
    return address

def process_tag(tag, css_result, tag_dict):
    tag = tag.replace('<span class="tag">', '').replace('</span>', '')
    items = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', tag, re.S)
    for item in items:
        if item in css_result:
            # 获取x, y坐标
            x, y = re.search('\.%s{background:-(\d+).0px -(\d+).0px;}' % item, css_result, re.S).group(1, 2)
            # print(x, y)
            for num in list(tag_dict.keys()):
                if int(y) > int(num):
                    continue
                else:
                    offset = int(int(x) / 12) + 1
                    #print('{}所在行第{}列'.format(num, offset))
                    str = tag_dict[num]
                    word = str[offset - 1]
                    tag = re.sub('<svgmtsi class="%s"></svgmtsi>' % item, word, tag)
                    break
            continue
    return tag

def svg_result(css_link):
    resp = requests.get(css_link)
    # print(resp.text)
    svg_links = re.findall('.*?background-image: url\((.*?svgtextcss.*?.svg)\)', resp.text)
    print(svg_links)

    num_dict = {}
    address_list = []
    tag_dict = {}
    for index, svg_link in enumerate(svg_links):
        svg_link = 'http:' + svg_link
        print(svg_link)
        respo = requests.get(svg_link)
        # print(respo.text)
        soup = BeautifulSoup(respo.text, 'lxml')
        if index == 0:
            nums = soup.select('text')
            for num in nums:
                y = num['y']
                num = num.get_text()
                num_dict[y] = num
            print(num_dict)
        elif index == 1:
            lis = soup.select('textPath')
            for li in lis:
                word = li.get_text()
                address_list.append(word)
            print(address_list)
        else:
            lis = soup.select('text')
            for li in lis:
                y = li['y']
                word = li.get_text()
                tag_dict[y] = word
            print(tag_dict)
    return num_dict, address_list, tag_dict

if __name__ == '__main__':
    pass