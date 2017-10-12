#-*-coding:utf8-*-

import requests
from lxml import etree

cook = {"Cookie": ""} #此处请填写你获取到的Cookie
url = 'http://weibo.cn/u/1890493665' #此处请修改为微博网址
# html = requests.get(url).content
# print html
html = requests.get(url, cookies = cook).content
# # html = requests.get(url, cookies = cook).text
#
# # html = bytes(bytearray(html, encoding='utf-8'))
selector = etree.HTML(html)
content = selector.xpath('//span[@class="ctt"]')
for each in content:
    text = each.xpath('string(.)')
    b = 1
    print text
