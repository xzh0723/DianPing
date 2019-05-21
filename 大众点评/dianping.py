from proxy import get_random_proxy
import pymongo
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
        #self.session = Session()

        # 数据库
        self.client = pymongo.MongoClient(host=MONGO_URI, port=MONGO_PORT)
        self.db = self.client.dazp

    def run(self):
        """
        遍历页码，提取数据  仅测试第一页
        """
        for page in range(1, 2):
            try:
                res = requests.get(self.url.format(page), headers=self.headers)
                print(res)
                if res.status_code == 200:
                    css_link = 'http:' + re.findall('.*?href="(.*?.svgtextcss.*?)"', res.text)[0]
                    css_result = requests.get(css_link).text
                    num_dict, address_dict, line_dict, tag_dict = dsvg_result(css_link)
                    html = res.text
                    soup = BeautifulSoup(html, 'lxml')
                    shop_list = soup.select('#shop-all-list')[0].find('ul').find_all('li')
                    # print(shop_list)
                    for shop in shop_list:
                        data = parse_data(shop, css_result, num_dict, address_dict, line_dict, tag_dict)
                        self.mongodb(data)

                        # 进入全部评论页面，仅测试第一页
                        comment_url = data['src'] + '/review_all/p1'
                        try:
                            res = requests.get(comment_url, headers=self.headers)
                            if res.status_code == 200:
                                # html = etree.HTML(res.text)
                                selector = Selector(text=res.text)
                                phone_info = selector.xpath('//div[@class="phone-info"]//text()').extract()
                                phone_number = process_phone_number(phone_info)
                                print(phone_number.strip())
                                # data['phone_number'] = phone_number.strip().replace('\xa0', ' ')
                                css_link = 'http:' + re.findall('.*?href="(.*?.svgtextcss.*?)"', res.text)[0]
                                # print(css_link)
                                resp = requests.get(css_link)
                                # print(resp.text)
                                css_result = resp.text
                                comment_dict = svg_result(css_result)
                                comments = selector.css('.reviews-items > ul > li')
                                for comment in comments:
                                    comment = parse_comment(comment, css_result, comment_dict)
                                    print(comment)
                                    self.mongodb(comment)
                        except Exception as e:
                            print('抓取评论页失败:', e.args)
            except Exception as e:
                print('抓取失败:', e.args)
                print('切换浏览器重试')
                self.run()

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
