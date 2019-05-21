# -*- coding:utf-8 -*-

import re
from bs4 import BeautifulSoup
import requests

def parse_data(shop, css_result, num_dict, address_dict, line_dict, tag_dict):
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
    # 处理数字部分，看具体用process_num 还是process_bumber 现在我这边要用的是process_num
    # 评论数
    # comment_num = shop.select('.review-num b')[0].get_text()
    # data['comment_num'] = process_number(comment_num)
    comment_num = str(shop.select('.review-num b')[0])
    #print(comment_num)
    data['comment_num'] = process_num(comment_num, css_result, num_dict)
    # 人均价
    # average_cost = shop.select('.mean-price b')[0].get_text()
    # data['average_cost'] = process_number(average_cost)
    average_cost = str(shop.select('.mean-price b')[0])
    #print(average_cost)
    data['average_cost'] = process_num(average_cost, css_result, num_dict)
    # 口味
    # sanitation_score = shop.select('.comment-list span:nth-child(1) b')[0].get_text()
    # data['sanitation_score'] = process_number(sanitation_score)
    sanitation_score = str(shop.select('.comment-list span:nth-child(1) b')[0])
    #print(sanitation_score)
    data['sanitation_score'] = process_num(sanitation_score, css_result, num_dict)
    # 环境
    # environment_score = shop.select('.comment-list span:nth-child(2) b')[0].get_text()
    # data['environment_score'] = process_number(environment_score)
    environment_score = str(shop.select('.comment-list span:nth-child(2) b')[0])
    # print(enviroment_score)
    data['environment_score'] = process_num(environment_score, css_result, num_dict)
    # 服务
    # service_score = shop.select('.comment-list span:nth-child(3) b')[0].get_text()
    # data['service_score'] = process_number(service_score)
    service_score = str(shop.select('.comment-list span:nth-child(3) b')[0])
    # print(service_score)
    data['service_score'] = process_num(service_score, css_result, num_dict)
    # 推荐菜
    data['recommend'] = shop.select('.recommend')[0].get_text().replace('\n', ' ')
    # 标签
    tag = str(shop.select('.tag-addr a:nth-child(1) .tag')[0])
    data['tag'] = process_tag(tag, css_result, line_dict, tag_dict)
    # 所处区域
    area = str(shop.select('.tag-addr a:nth-child(3) .tag')[0])
    data['area'] = process_tag(area, css_result, line_dict, tag_dict)
    # 地址
    xaddress = str(shop.select('.addr')[0])
    data['address'] = process_address(xaddress, css_result, address_dict)
    return data

def process_number(number):
    """
    处理数字
    注：前两天爬大众点评的时候，他的数字还是用的svg矢量图替换，但是我爬多了之后就变成了字体资源替换了，不知道是不是一种反爬措施
    所以其实大众点评最核心的反爬还是IP限制跟cookies限制，解决了这两个问题就OK了
    """
    number_dict = {
        '\ue573': '1', '\ue3a3': '2', '\uf759': '3', '\uf831': '4', '\ue2ba': '5', '\ue96b': '6', '\ue7d4': '7',
        '\uf8d6': '8', '\ueb25': '9', '\uee53': '0'
    }
    for i in list(number_dict.keys()):
        if i in number:
            number = number.replace(i, number_dict[i])
    return number

def process_num(process_num, css_result, num_dict):
    """
    处理数字
    注：如果你获取的svg文件有三个，请把下方的svg_result中的number_dict开启，然后处理数字用这个函数
    嗯，我昨天爬的时候数字这部分换成字体资源了，今天又变成svg替换了。。  可怕
    """
    items = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', process_num, re.S)
    process_num = re.sub('</b>', '', re.sub('<b>', '', process_num))
    for item in items:
        if item in css_result:
            # 获取x, y坐标
            x, y = re.search('\.%s{background:-(\d+).0px -(\d+).0px;}' % item, css_result, re.S).group(1, 2)
            #print(x, y)
            if int(y) <= int(list(num_dict.keys())[0]):
                offset = int((int(x) + 5) / 12)
                #print('第{}行第{}列'.format(1, offset))
                str = list(num_dict.values())[0]
                num = str[offset - 1]
                #print(num)
                process_num = re.sub('<svgmtsi class="%s"></svgmtsi>' % item, num, process_num)
                # print(tag + ':' + num)
            elif int(y) <= int(list(num_dict.keys())[1]):
                offset = int((int(x) + 5) / 12)
                #print('第{}行第{}列'.format(2, offset))
                str = list(num_dict.values())[1]
                num = str[offset - 1]
                #print(num)
                process_num = re.sub('<svgmtsi class="%s"></svgmtsi>' % item, num, process_num)
            else:
                offset = int((int(x) + 5) / 12)
                #print('第{}行第{}列'.format(3, offset))
                str = list(num_dict.values())[2]
                num = str[offset - 1]
                #print(num)
                process_num = re.sub('<svgmtsi class="%s"></svgmtsi>' % item, num, process_num)
    return process_num

def process_address(address, css_result, address_dict):
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
                    offset = int(int(x) / 12) + 1
                    #print('{}所在行第{}列'.format(num, offset))
                    str = address_dict[num]
                    word = str[offset - 1]
                    address = re.sub('<svgmtsi class="%s"></svgmtsi>' % item, word, address)
                    break
            continue
    return address

def process_tag(tag, css_result, line_dict, tag_dict):
    """
    处理标签信息
    """
    tag = tag.replace('<span class="tag">', '').replace('</span>', '')
    items = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', tag, re.S)
    for item in items:
        if item in css_result:
            # 获取x, y坐标
            x, y = re.search('\.%s{background:-(\d+).0px -(\d+).0px;}' % item, css_result, re.S).group(1, 2)
            #print(x, y)
            for number in list(line_dict.keys()):
                if int(y) > int(number):
                    continue
                else:
                    line = line_dict[number]
                    str = tag_dict[line]
                    offset = int(int(x) / 12) + 1
                    #print('第{}行第{}列'.format(line, offset))
                    word = str[offset - 1]
                    tag = re.sub('<svgmtsi class="%s"></svgmtsi>' % item, word, tag)
                    break
            continue
    return tag

def dsvg_result(css_link):
    """
    解析svg链接，获取替换字典
    """
    res = requests.get(css_link)
    # print(resp.text)
    svg_links = re.findall('.*?background-image: url\((.*?svgtextcss.*?.svg)\)', res.text)
    print(svg_links)

    tag_dict = {}
    address_dict = {}
    num_dict = {}
    line_dict = {}
    for index, svg_link in enumerate(svg_links):
        svg_link = 'http:' + svg_link
        print(svg_link)
        response = requests.get(svg_link)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        # 如果你获取的svg文件有三个，那么说明数字也是svg矢量图替换，请将下面的注释去掉，将第二个index改成==1，获取num_dict并返回
        if index == 0:
            paths = soup.find_all('path')
            for path in paths:
                id_ = path['id']
                number = path['d'].split(' ')[1]
                line_dict[number] = id_
            print(line_dict)
            lis = soup.select('textPath')
            for li in lis:
                #    y = li['y']
                num = li['xlink:href'].replace('#', '')
                word = li.get_text()
                tag_dict[num] = word
            print(tag_dict)
        elif index == 1:
            lis = soup.select('text')
            # print(lis)
            for li in lis:
                y = li['y']
                word = li.get_text()
                address_dict[y] = word
            print(address_dict)
        else:
            nums = soup.select('text')
            for num in nums:
                # print(num)
                y = num['y']
                num = num.get_text()
                num_dict[y] = num
            print(num_dict)
    return num_dict, address_dict, line_dict, tag_dict

if __name__ == '__main__':
    pass