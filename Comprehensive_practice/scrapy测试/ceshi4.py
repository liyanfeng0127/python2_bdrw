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

def deep_pasre_url(all_url, start_url, deeplevel):
    if start_url:
        n = deeplevel
        while n:
            all_url2 = []
            all_url3 = []
            for i in range(len(start_url)):
                html = requests.get(start_url[i]).content
                selector = etree.HTML(html.decode('utf-8'))
                parse_url2 = selector.xpath("//a[contains(@href,'http')]/@href")
                parse_url3 = selector.xpath("//a[contains(@href,'https')]/@href")
                for http_url2 in parse_url2:
                    all_url2.append(http_url2)
                for http_url3 in parse_url3:
                    all_url3.append(http_url3)
            n -= 1
            start_url = [] + all_url2 + all_url3
            print start_url
            all_url = all_url + list(set(all_url2 + all_url3))
            print all_url
            return deep_pasre_url(all_url, start_url, n)
        return all_url
    else:
        return 'the starturl is none!'





if __name__ == '__main__':
    all_url = [u'http://i.dxy.cn/profile/\u6ca1\u7f51\u540d\u4e86']
    start_url = [u'http://i.dxy.cn/profile/\u6ca1\u7f51\u540d\u4e86']
    post_url = deep_pasre_url(all_url, start_url,deeplevel=2)

#u'http://i.dxy.cn/profile/\u6ca1\u7f51\u540d\u4e86'