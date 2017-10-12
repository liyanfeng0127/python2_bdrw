# -*- coding: utf-8 -*-

from lxml import etree
import requests
import sys
import pymongo
from multiprocessing.dummy import Pool as ThreadPool

reload(sys)

sys.setdefaultencoding('utf-8')

connection = pymongo.MongoClient()
tdb = connection.Zongheshijian
post_info = tdb.test

#下载到mongo库中
def InsertOne(one):
    post_info.insert(one)

#内容下载到yixuelunwen.txt
def towrite(parm):
    f.writelines(u'回帖题目：' + str(parm['discuss_title']) + '\n')
    f.writelines(u'回帖网址：' + str(parm['discuss_website']) + '\n\n')


def spider(url):
    #解析网页
    agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'
    }
    #如果请求网页之后是500，那么久需要加header
    header = {
        "HOST":"www.dxy.cn",
        "Referer":"http://www.dxy.cn/",
        'User-Agent':agent
    }
    html = requests.get(url, headers=header).content
    selector = etree.HTML(html.decode('utf-8'))
    #用xpath解析html文件，并生成一个列表
    forum = selector.xpath('//div[@id="col-1"]/table[@class="post-table"]/tbody/tr')
    print forum
    item = {}
    for each in forum:
        forum_first = each.xpath('td[@class="news"]/a[starts-with(@href,"http")]')[0]
        #当class内容较多时，可以只选取一段使用，语法使用为//div[contains(@class,"post-table)"]
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


if __name__ == '__main__':
    #启动多线程
    pool = ThreadPool(4)
    f = open('yixueluntan2.txt','a')
    #得到多个网页地址
    page = []
    for i in range(1,10):
        newpage = 'http://www.dxy.cn/bbs/board/103?order=2&tpg=' + str(i)
        page.append(newpage)
    results = pool.map(spider, page)
    pool.close()
    pool.join()
    f.close()