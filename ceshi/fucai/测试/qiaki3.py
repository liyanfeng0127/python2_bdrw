#-*-coding:utf8-*-

import sys
from lxml import etree
import requests
import sys
import re
import pymongo
from multiprocessing.dummy import Pool as ThreadPool
from scrapy.http import Request
import time
from lxml import html


reload(sys)
sys.setdefaultencoding('utf-8')

def parse_detail(url):
    old_number = []
    xml = requests.get(url).content
    #selector = etree.HTML(xml.decode('utf-8'))
    selector = html.fromstring(xml)
    # numbers = selector.find_class("odd")
    # for number in numbers:
    #     old_number.append(number.xpath("./td/text()"))
    numbers = selector.find_class("")
    for number in numbers:
        old_number.append(number.xpath("./td/text()")[0])
    print old_number



if __name__ == '__main__':
    second_url = 'http://www.bwlc.gov.cn/bulletin/prevkeno.html'
    a = parse_detail(second_url)