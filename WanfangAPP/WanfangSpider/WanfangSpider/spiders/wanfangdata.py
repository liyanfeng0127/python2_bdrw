# -*- coding: utf-8 -*-
import scrapy
import re
from lxml import etree
import requests
import sys
import pymongo
from multiprocessing.dummy import Pool as ThreadPool
from scrapy.http import Request
from urllib import parse
from WanfangSpider.items import WanfangspiderItem,WanfangspiderTxtItem
from WanfangSpider.ultil.command import get_md5
import datetime
from scrapy.loader import ItemLoader
try:
    import cookielib
except:
    import http.cookiejar as cookielib


reload(sys)
sys.setdefaultencoding('utf-8')


class WanfangdataSpider(scrapy.Spider):
    name = "wanfangdata"
    allowed_domains = ["wanfangdata.com.cn"]
    start_urls = ['http://www.wanfangdata.com.cn/']
    deep_number = 1
    all_url = start_urls
    image_url = []session = requests.session()
    # session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
    # try:
    #     session.cookies.load(ignore_discard=True)
    # except:
    #     print ("cookie未能加载")




    def parse(self, response):
        #获取原始网页中所有url
        #1.获取文章列表页中的URL并交给scrapy下载后进行解析
        #2.获取下一页的url并交给scrapy进行下载
    #解析列表中的所有URL并交给scrapy下载后解析
        self.start_urls = []
        try:
            parse_urls = response.xpath("//a[contains(@href,'http')]/@href | a[contains(@href,'https')]/@href")
            for parse_url in list(set(parse_urls)):
                if parse_url.root not in self.all_url:
                    self.start_urls.append(parse_url.root)
                    self.all_url.append(parse_url.root)
        except:
            print("the url is error!")

        if self.start_urls:
            if self.deep_number:
                self.deep_number -= 1
                #提取下一页URL并交给scrapy进行下载
                for deepurl in self.start_urls:
                    #meta= 是传递给callback的其他参数的
                    yield Request(url=urlparse.urljoin(response.url, str(deepurl)), meta={"start_urls":self.start_urls}, callback=self.parse)
            # 获取所有原始网页的URL，并进行scrapy解析
            else:
               for alldeepurl in self.all_url:
                   yield Request(url=str(alldeepurl), meta={"all_urls": self.all_url}, callback=self.parse_detail)



    def parse_detail(self,response):
        #对具体网页进行解析，并存入到MySQL数据库中
        wanfangdata = WanfangspiderItem()

        #获取网页url，并对其url进行配置id
        wanfangdata["url_object_id"] = get_md5(response.url)

        #获取网页文本的图像
        try:
            image_urls = response.xpath("//img/@src").extract()
            for images in image_urls:
                http_url = urlparse.urljoin(response.url, images)
                if http_url not in self.image_url:
                    self.image_url.append(http_url)
            wanfangdata["image_url"] = self.image_url

        except :
            print "the IMAGE_URL is fail!"


        try:
            #获取网页题目
            title = response.xpath("/html/head/title/text()").extract()
            if title:
                title = title[0].encode('utf-8')
                wanfangdata["title"] = title

        except :
            print "the TITLE is fail!"

        try:
            #首先判断网页编码的方式
            encode_method = response.xpath("/html/head/meta[@content,'utf-8']/@content")
            #如果是utf-8编码格式，进行encode('utf-8')格式转换
            if len(encode_method):
                # 获取网页关键词/html/head/meta[3]
                spider_keywords = response.xpath("/html/head/meta[@name='keywords']/@content")
                if spider_keywords:
                    for keyword in spider_keywords:
                        if isinstance(keyword.root, unicode):
                            wanfangdata["spider_keyword"] = str(keyword.root).encode('utf-8')
                else:
                    wanfangdata["spider_keyword"] = '0'
            else:
                spider_keywords = response.xpath("/html/head/meta[@name='keywords']/@content")
                if spider_keywords:
                    for keyword in spider_keywords:
                        if isinstance(keyword.root, unicode):
                            wanfangdata["spider_keyword"] = str(keyword.root).decode('utf-8').encode('gbk')
                else:
                    wanfangdata["spider_keyword"] = '0'

        except :
            print "the KEYWORDS is fail!"

        try:
            #获取网页描述
            description = response.xpath("/html/head/meta[@name='description']/@content")
            if description:
                for des in description:
                    if isinstance(des.root, unicode):
                        wanfangdata["description"] = str(des.root.encode('utf-8'))

        except:
            print "the DESCRIPTION is fail!"

        try:
            # 获取网页文本内容
            url_contents = list(response.xpath("//text()"))
            url_content = []
            url_str = str()
            for filedata in url_contents:
                if isinstance(filedata.root, unicode):
                    data_utf8 = filedata.root.encode('utf-8')
                    url_content.append(data_utf8)
            for i in range(len(url_content)):
                url_str += url_content[i] + ','
            wanfangdata["url_content"] = url_str

        except:
            print "the URL_CONTENT is fail!"

        try:
            #获取爬行网页的url
            spider_url = response.url
            wanfangdata["spider_url"] = spider_url

        except :
            print "the SPIDER_URL is fail!"

        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # wangfangdata["create_date"] = create_date
        #wangfangdata["url_images"] = [url_images]

        # #通过itemloader加载item
        # item_loader = ItemLoader(item=WanfangspiderItem(), response= response)
        # item_loader.add_xpath("title", "/html/head/title/text()")
        # item_loader.add_value("url", response.url)
        # wanfangdata = item_loader.load_item()

        #对具体网页进行解析，并存入到txt格式文件中
        # wanfangdata_txt = WanfangspiderTxtItem()
        # # 从parse函数中的callback调用过来的参数，用meta即可展现
        # all_urls = response.meta.get("all_urls", "")
        # wanfangdata_txt["all_urls"] = all_urls

        try:
            all_urls = response.meta.get("all_urls", "")
            wanfangdata["all_urls"] = all_urls

        except:
            print "the ALL_URLS is failed!"

        # self.session.cookies.save()

        yield wanfangdata
        # yield wanfangdata_txt



