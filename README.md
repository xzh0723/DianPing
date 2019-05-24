大众点评店铺信息爬虫

  破解大众点评svg矢量图与字体资源替换反爬。

项目目录

│  config.py
│  parse_dianpu.py
│  parse_comment.py
│  dianping.py
│  proxy.py
│  README.md
│  ua.log
│
└─view
        analysis*.png
        db.png
        
环境依赖

python 3.7.2

抓取流程

  美食店铺首页开始，遍历抓取每页内容，获取店铺详情连接，构造全部评论API抓取全部评论。

反爬

  大众点评的反爬措施很强，可以ban掉大部分爬虫。当然，误伤率也比较高。测试期间发现的反爬措施有：

常规链接404（店铺详情页链接404页面）
请求头校验
多类型字体反爬（偏移量，自定义css）
验证码（常规四字中英文混合）
cookies
ban ip
  大众点评总的来说还是基于IP检测，爬虫的重点在于：代理IP的质量。

反反爬

挂代理（代理池随机获取可用代理）
Headers 添加随机 UA 和 Refer 参数
随机抓取时延


解释说明

按崔大的框架搭建的代理池，抓取网络各大免费代理网站，可用代理少，代理成活率低，效率慢，建议使用付费代理或者ADSL拨号代理。

运行

  命令行切换至根目录：

>>> python dianping.py
抓取结果

![image](https://github.com/xzh0723/dzdp/blob/master/view/db_dianpu.png.png)

公告

  本代码仅作学习交流，切勿用于商业用途，否则后果自负。若涉及点评网侵权，请邮箱联系，会尽快处理。
