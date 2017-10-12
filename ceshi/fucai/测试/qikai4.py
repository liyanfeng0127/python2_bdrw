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
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def parse_detail(url):
    head = {'User-Agent':
                'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    old_number = []
    xml = requests.get(url,headers=head).content
    print xml



if __name__ == '__main__':
    second_url = 'http://www.bwlc.gov.cn/bulletin/prevkeno.html'
    page_url = 'http://www.bwlc.gov.cn/bulletin/prevkeno.html?page=2'
    a = parse_detail(page_url)