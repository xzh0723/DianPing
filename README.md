大众点评店铺信息爬虫
=======

  破解大众点评svg矢量图与字体资源替换反爬。

项目目录
-------
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
---------
python 3.7.2

抓取流程
-------
  美食店铺首页开始，遍历抓取每页内容，获取店铺详情连接，构造全部评论API抓取全部评论。

反爬
--------
  大众点评的反爬措施很强，可以ban掉大部分爬虫。当然，误伤率也比较高。测试期间发现的反爬措施有：

常规链接404（店铺详情页链接404页面）

请求头校验

多类型字体反爬（偏移量，自定义字体）

验证码（常规四字中英文混合）

cookies

ban ip
>>大众点评总的来说还是基于IP检测，爬虫的重点在于：代理IP的质量。

反反爬
--------
>>svg偏移量：
>>>>源码中可见部分文字和数字被svgmtsi标签替换，点击标签在控制台右侧style内可知css样式内容。其中有替换映射xy值的css连接和文字字典svg连接。css链接可以在源码中正则匹配获取，svg连接在css链接的文件中也可以正则匹配获取。每个svgmtsi的class属性在css链接文件中都有唯一的xy值映射，通过正则匹配获取xy值。xy值的作用就是对应svg文件中的文字偏移量，即第几行第几列。行数的获取分两种情况：第一种是svg文件源码中的text标签内含有y属性，这种情况真实文字所在行数对应为css文件内匹配的y值刚好大于text标签内的y值的那一行；第二种情况为指定了文字的height，height与y值之间存在数学关系。得出行数即得到了真实文字所在的字符串，接下来只需得出x偏移量即列数（字符串索引值）即可获取真实文字。测试发现x与偏移量之间也存在特定的数学关系，为x / width + 1，这些数学关系均可能发生变化，需自行探索。svg文件至少存在一个，最多存在三个。店铺列表页存在三个时，分别对应数字/地址/标签；评论页存在三个时，分别对应数字/地址/评论。注：svg链接的获取顺序会随时变化，需自行更换。

>>自定义字体资源替换：
>>>>同一个css链接，当换成字体资源替换时，获取字体文件链接下载，用百度字体编辑器打开查看字体映射，制作映射表，动态替换即可。

注： 同一个IP爬取次数过多时，会出现svg偏移和字体资源替换动态交替。

>>挂代理（代理池随机获取可用代理）

>>cookies

>>Headers 添加随机 UA 和 Refer 参数

>>随机抓取延迟

解释说明
--------
>>按崔大的框架搭建的代理池，抓取网络各大免费代理网站，可用代理少，代理成活率低，效率慢，建议使用付费代理或者ADSL拨号代理。
>>另外如需大量抓取，需建立cooki池，防止因同一个账号抓取次数过多被ban。

运行
-------
  命令行切换至根目录：

>>> python dianping.py

抓取结果
--------
![image](https://github.com/xzh0723/dzdp/blob/master/view/db_dianpu.png.png)
![image](https://github.com/xzh0723/dzdp/blob/master/view/db_pinglun.png.png)
![image](https://github.com/xzh0723/dzdp/blob/master/view/pycharm_dianpu.png.png)
![image](https://github.com/xzh0723/dzdp/blob/master/view/pychram_dianpu.png.png)

公告
=========
  本代码仅作学习交流，切勿用于商业用途，否则后果自负。
