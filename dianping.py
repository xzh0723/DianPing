from proxy import get_random_proxy
import pymongo
import math
from parse_dianpu import *
from parse_comment import *
import requests
from config import *

class Dianping():

    def __init__(self):
        self.headers = HEADERS
        # self.proxies = {
        #     'http': 'http://{}'.format(get_random_proxy()),
        # }
        self.url = 'http://www.dianping.com/changsha/ch10/g104p{}'
        # self.session = Session()

        # 数据库
        self.client = pymongo.MongoClient(host=MONGO_URI, port=MONGO_PORT)
        self.db = self.client.dazp

    def run(self):
        """
        遍历页码，提取数据  仅测试一页
        """
        for page in range(3, 4):
            #try:
                res = requests.get(self.url.format(page), headers=self.headers)
                print(res)
                if res.status_code == 200:
                    # 获取店铺列表页的css链接，进一步获取svg链接，请求获取数字字典、地址字典、标签字典（这里标签字典包含两部分，line_dict是定位行数的）
                    css_link = 'http:' + re.findall('.*?href="(.*?.svgtextcss.*?)"', res.text)[0]
                    css_result = requests.get(css_link).text
                    num_dict, address_dict, address_list, line_dict, tag_dict = dsvg_result(css_link)

                    html = res.text
                    soup = BeautifulSoup(html, 'lxml')
                    shop_list = soup.select('#shop-all-list')[0].find('ul').find_all('li')
                    # print(shop_list)

                    # 如果在这个for循环内解析评论，会导致下一个店铺无法完成字符替换，不知道为什么。。
                    # 所以我单独用一个list封装店铺详情链接，用另一个for循环获取评论

                    # 解析获取店铺信息
                    src_list = []
                    for shop in shop_list:
                        data = parse_data(shop, css_result, num_dict, address_dict, address_list, line_dict, tag_dict)
                        print(data)
                        # self.mongodb(data)

                        # max_comment_page = math.ceil(int(data['comment_num']) / 15)
                        src_list.append(data['src'])

                    # print(src_list)
                    for src in src_list:
                        # print('爬取{}'.format(src))
                        # 进入全部评论页面，仅测试一页
                        for page in range(3, 4):
                            comment_url = src + '/review_all/p{}'.format(page)
                            # try:
                            res = requests.get(comment_url, headers=self.headers)
                            if res.status_code == 200:
                                selector = Selector(text=res.text)

                                # 获取评论详情页的css链接，进一步获取svg链接，请求获取评论字典
                                css_link = 'http:' + re.findall('.*?href="(.*?.svgtextcss.*?)"', res.text)[0]
                                # print(css_link)
                                resp = requests.get(css_link)
                                # print(resp.text)
                                css_result = resp.text
                                num_dict, address_dict, comment_dict = svg_result(css_result)

                                # 详情页获取店铺号码并插入店铺信息集合
                                phone_info = str(selector.css('p[class="expand-info tel"]').extract_first())
                                # phone_info = selector.xpath('//div[@class="phone-info"]//text()').extract()
                                phone_number = process_cnum(phone_info, css_result, num_dict)
                                print(phone_number.strip())

                                # 详情页获取详细地址
                                address_info = str(selector.css('#address').extract_first())
                                address = process_caddress(address_info, css_result, address_dict)
                                print(address)

                                comments = selector.css('.reviews-items > ul > li')
                                # 解析获取评论信息
                                for comment in comments:
                                    comment = parse_comment(comment, css_result, comment_dict)
                                    # print(comment)
                                    self.mongodb(comment)
                            # except Exception as e:
                            #    print('抓取评论页失败:', e.args)

            #except Exception as e:
            #    print('抓取失败:', e.args)
            #    print('切换浏览器重试')
            #    self.run()

    def mongodb(self, data):
        """
        存储数据
        """
        print(data)
        if data.get('comment'):
            collection = 'comment'
        else:
            collection = 'store'
        try:
            if self.db[collection].insert(dict(data)):
                print('成功插入数据库')
        except Exception as e:
            print('插入数据库失败：', e.args)

if __name__ == "__main__":
    dianping = Dianping()
    dianping.run()