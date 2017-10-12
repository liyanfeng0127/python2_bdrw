# -*- coding: utf-8 -*-

from lxml import etree
import requests
import sys
from multiprocessing.dummy import Pool as ThreadPool
import lxml.html as lhl

reload(sys)
sys.setdefaultencoding('utf-8')

FIELDS = ('company')

def spider(url):
    tree = lhl.fromstring(url)
    results = {}
    # for field in FIELDS:
    #     results[field] = tree.cssselect('#newlist_list_content_table > table:nth-child(2) > tbody > tr:nth-child(1) > td.gxsj > span')
    table = tree.cssselect('#newlist_list_content_table > table')
    return results




if __name__ == '__main__':

    # pool = ThreadPool(4)
    # f = open('ER_CSS.txt','a')
    page = []
    for i in range(1, 5):
        newpage = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&jl=北京&kw=嵌入式&sm=0&isfilter=1&fl=530&isadv=0&sb=1&sg=8de28363eb064a2b8ab40da3111bbceb&p=' + str(i)
        page.append(newpage)
    result = map(spider,page)
    print result
    # pool.close()
    # pool.join()
    # f.close()
