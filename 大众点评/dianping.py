from proxy import get_random_proxy
import pymongo
from parse_dianpu import *
from parse_comment import *
from lxml import etree
import requests
from config import *

class Dianping():

    def __init__(self):
        self.headers = HEADERS
        self.proxies = {
            'http': 'http://{}'.format(get_random_proxy()),
            'https': 'https://{}'.format(get_random_proxy())
        }
        self.url = 'http://www.dianping.com/changsha/ch10/g104p{}'
        #self.session = Session()

        # 数据库
        self.client = pymongo.MongoClient(host=MONGO_URI, port=MONGO_PORT)
        self.db = self.client.MONGO_DB

    def run(self):
        """
        遍历页码，提取数据
        """
        for page in range(1, 6):
            try:
                res = requests.get(self.url.format(page), headers=self.headers)
                if res.status_code == 200:
                    css_link = 'http:' + re.findall('.*?href="(.*?.svgtextcss.*?)"', res.text)[0]
                    css_result = requests.get(css_link).text
                    num_dict, address_list, tag_dict = svg_result(css_link)
                    html = res.text
                    soup = BeautifulSoup(html, 'lxml')
                    shop_list = soup.select('#shop-all-list')[0].find('ul').find_all('li')
                    #print(shop_list)
                    for shop in shop_list:
                        data = parse_data(shop, css_result, num_dict, address_list, tag_dict)
                        self.mongodb(data)

                        # 进入全部评论页面
                        comment_url = data['src'] + '/review_all'
                        try:
                            res = requests.get(comment_url, headers=self.headers)
                            if res.status_code == 200:
                                comment = parse_comment(res.text)
                                # print(comment)
                                self.mongodb(comment)
                        except Exception as e:
                            print('抓取评论页失败:', e.args)
            except Exception as e:
                print('抓取失败:', e.args)

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