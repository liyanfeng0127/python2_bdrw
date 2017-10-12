#-*-coding:utf8-*-

from lxml import etree
import requests
import sys
import re
import pymongo
from multiprocessing.dummy import Pool as ThreadPool
from scrapy.http import Request
import time

reload(sys)
sys.setdefaultencoding('utf-8')

#解析URL，并进行深度采集网页
def deep_pasre_url(all_url, start_url, deeplevel):
    if start_url:
        n = deeplevel
        while n:
            all_url2 = []
            all_url3 = []
            for i in range(len(start_url)):
                html = requests.get(start_url[i]).content
                #selector = etree.HTML(html.decode('utf-8'))
                selector = etree.HTML(html)
                parse_url2 = selector.xpath("//a[contains(@href,'http')]/@href")
                parse_url3 = selector.xpath("//a[contains(@href,'https')]/@href")
                for http_url2 in parse_url2:
                    all_url2.append(http_url2)
                for http_url3 in parse_url3:
                    all_url3.append(http_url3)
            n -= 1
            # start_url = [] + parse_url2 + parse_url3
            start_url = [] + all_url2 + all_url3
            print start_url
            all_url = all_url + list(set(all_url2 + all_url3))
            print all_url
            return deep_pasre_url(all_url, start_url, n)
        return all_url
    else:
        return 'the starturl is none!'

#读取配置文件
def readtxt_url(path):
    start_url = []
    with open(path) as read_url:
        try:
            for init_url in read_url.readlines():
                start_url.append(init_url)
            return start_url
        except:
            print "read the file is error!"
        finally:
            read_url.close()



if __name__ == '__main__':
    path = u'G://PyCharm//data//配置文件.csv'
    start_url = readtxt_url(path)
    all_url = start_url
    inittime = time.time()
    post_url = deep_pasre_url(all_url, start_url,deeplevel=2)
    endtime = time.time()
    a = endtime - inittime
    print u"运行时间为： %s" % a
