#-*-coding:utf8-*-

from lxml import etree
import requests
import sys
import re
import pymongo
from multiprocessing.dummy import Pool as ThreadPool
from scrapy.http import Request

reload(sys)
sys.setdefaultencoding('utf-8')

def spider(url):
    #解析网页
    html = requests.get(url).content
    selector = etree.HTML(html.decode('utf-8'))
    selector = selector.xpath("//a[contains(@href,'http')][@href]")
    print selector

if __name__ == '__main__':
    page = ['http://www.dxy.cn/bbs/board/103?order=2&tpg=1']
    result = requests.get(url=page[0]).content
    all_url = []
    # @"((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?"
    regex = re.compile("((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?")
    all_url2 = re.search("((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?",result)
    print all_url2
    all_url = regex.findall(result)
    for i in all_url:
        i.replace(',', '.')
        print i