# -*- coding: utf-8 -*-
from lxml import etree
import requests
import sys
from multiprocessing.dummy import Pool as ThreadPool

reload(sys)
sys.setdefaultencoding('utf-8')

def spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//div[@id="j_p_postlist"]/div')
    item = {}
    for each in content_field:
        content = each.xpath('//div[starts-with(@id,"post_content_")]/text()')
        item['context'] = content
    return item


if __name__ == '__main__':
    page = []
    for i in range(1,21):
        newpage = 'http://tieba.baidu.com/p/3522395718?pn=' + str(i)
        page.append(newpage)
    results = map(spider, page)
    print results