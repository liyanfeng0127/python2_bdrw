# -*- coding: utf-8 -*-

from lxml import etree
import requests
import sys
import pymongo
from multiprocessing.dummy import Pool as ThreadPool

reload(sys)

sys.setdefaultencoding('utf-8')

connection = pymongo.MongoClient()
tdb = connection.shijian
post_info = tdb.test

#下载到mongo库中
def InsertOne(one):
    post_info.insert(one)

#内容下载到yixuelunwen.csv
def towrite(parm):
    f.writelines(u'回帖题目：' + str(parm['discuss_title']) + '\n')
    f.writelines(u'回帖网址：' + str(parm['discuss_website']) + '\n\n')


def spider(url):
    #解析网页
    html = requests.get(url).content
    selector = etree.HTML(html.decode('utf-8'))
    #用xpath解析html文件，并生成一个列表
    forum = selector.xpath('//div[@id="col-1"]/table[@class="post-table"]/tbody/tr')
    item = {}
    for each in forum:
        forum_first = each.xpath('td[@class="news"]/a[starts-with(@href,"http")]')[0]
        print forum_first
        forum_first = list(forum_first.xpath('string(.)'))
        #将一个个字符整合到一个字符串
        forum_first = ''.join(forum_first)
        forum_net = each.xpath('td[@class="news"]/span[@class="pag"]/a/@href')
        if forum_net :
            item['discuss_website'] = forum_net
        else :
            forum_net = each.xpath('td[@class="news"]/a/@href')
            item['discuss_website'] = forum_net
        item['discuss_title'] = forum_first
        towrite(item)
    InsertOne(item)
    #通过递归获取网页地址
    nextlink = selector.xpath('//div[@id="col-1"]/div[@class="rfloat mt10"]/div[@class="pages"]/div[@class="next_h"]/a/@href')
    if nextlink:
        nextlink = nextlink[0]
        print nextlink
        spider(nextlink)


if __name__ == '__main__':
    #启动多线程
    pool = ThreadPool(4)
    f = open('yixueluntan_digui.csv','a')
    page = ['http://www.dxy.cn/bbs/board/103?order=2&tpg=1']
    result = pool.map(spider,page)
    pool.close()
    pool.join()
    f.close()