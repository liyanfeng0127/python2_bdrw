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


start_url = ['http://www.dxy.cn/bbs/board/103?order=2&tpg=1']

#for every_url in all_url:
#html = requests.get(start_url[i] for i in range(len(start_url))).content

#穿入url列表，可以获取累加式的新url列表
def deep_pasre_url(start_url):
    all_url = []
    for i in range(len(start_url)):
        html = requests.get(start_url[i]).content
        selector = etree.HTML(html.decode('utf-8'))
        all_url2 = selector.xpath("//a[contains(@href,'http')]/@href")
        all_url3 = selector.xpath("//a[contains(@href,'https')]/@href")
        all_url = all_url + list(set(all_url2 + all_url3))
        print all_url

def parse_url(url):
    data_url = list(url)
    html = requests.get(url).content
    selector = etree.HTML(html.decode('utf-8'))
    keywords = selector.xpath("/html/head/meta[@name='keywords']/@content")
    data_item = {}
    if keywords:
        keywords = keywords[0].encode('utf-8')
        data_item['keywords'] = keywords

    description = selector.xpath("/html/head/meta[@name='description']/@content")
    #url_content = ''.join(keywords).split()

        #.replace(' ', '')
    return data_item


if __name__ == '__main__':
    second_url = ['http://www.wanfangdata.com.cn/']
    url_content = parse_url(second_url[0])
    with open('ceshi_content.txt', 'wt') as af:
        af.writelines(url_content)
    af.close()
    print url_content



