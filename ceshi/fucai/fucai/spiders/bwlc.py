# -*- coding: utf-8 -*-
import scrapy
from fucai.items import FucaiItem
import re
from scrapy.http import Request

class BwlcSpider(scrapy.Spider):
    name = "bwlc"
    allowed_domains = ["bwlc.gov.cn"]
    start_urls = ['http://www.bwlc.gov.cn/bulletin/prevkeno.html']
    all_number = []

    def parse(self, response):
        a = response.body
        if len(self.all_number):
            qishu_List = re.findall(r'<td>([\d]{6})<\/td>', response.body)
            if len(qishu_List):
                if qishu_List[0] in self.all_number:
                    pass
                else:
                    self.all_number.append(qishu_List[0])


        #当第一次爬取时候进行全部抓取，并存入到txt文件
        else:
            qishuList = re.findall(r'<td>([\d]{6})<\/td>', response.body)
            if len(qishuList):
                for qishu in qishuList:
                    self.all_number.append(qishu)
                yield Request(url=self.start_urls[0], meta={"all_number": self.all_number}, callback=self.parse_detail)

#解析全部数据
    def parse_detail(self,response):
        fucai = FucaiItem()
        qishuList = response.meta.get("all_number", "")
        fucai["name"] = qishuList

        yield fucai
        yield Request(url=self.start_urls[0], callback=self.parse_fucai_again)

    def parse_one_data(self,response):
        fucai = FucaiItem()
        qishuList = response.meta.get("all_number", "")
        fucai["name"] = qishuList

        yield fucai
        yield Request(url=self.start_urls[0], callback=self.parse_fucai_again)

    def parse_fucai_again(self,response):
        yield Request(url=self.start_urls[0], callback=self.parse)



