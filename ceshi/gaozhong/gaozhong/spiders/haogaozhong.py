# -*-coding:utf8-*-

import scrapy
import re
from lxml import etree
import requests
import sys
import pymongo
from multiprocessing.dummy import Pool as ThreadPool
from scrapy.http import Request
from urllib import parse
import urlparse
from lxml import html
from gaozhong.items import GaozhongItem
from gaozhong.ultil.command import get_md5

reload(sys)
sys.setdefaultencoding('utf-8')


class HaogaozhongSpider(scrapy.Spider):
    name = "haogaozhong"
    allowed_domains = ["haogaozhong.eol.cn"]
    url_join = ['http://haogaozhong.eol.cn']
    start_urls = ['http://haogaozhong.eol.cn/school_area.php']
    province_number_urls = []
    city_number_urls = []
    town_number_urls = []
    all_urls = []

    def parse(self, response):
        #通过循环解析每个URL的内容
        yield Request(url=response.url, dont_filter=True, callback=self.parse_url_detail)
    #解析市级url
    # def parse_url_city(self,response):
    #     #/html/body/div[6]/div[1]/div[1]/div[6]/ul/li[1]/a[9]
    #     xml = response.xpath("/html/body/div[6]/div[1]/div[1]/div[6]/ul/li/a/@value")
    #     for i in xml:
    #         self.city_number_urls.append(response.url + '&city=' + i.root)
    #     for url in self.city_number_urls:
    #         yield Request(url=url, callback=self.parse_url_town)
    #解析镇一级相关url
    # def parse_url_town(self,response):
    #     #//*[@id="town"]/a[5]
    #     xml = response.xpath("//p[@id='town']/a/@value")
    #     for i in xml:
    #         self.town_number_urls.append(response.url + '&town=' + i.root)
    #     for url in self.town_number_urls:
    #         yield Request(url=url, callback=self.parse_url_detail)


    def parse_url_detail(self, response):
        #实例化，与items建立联系
        haogaozhong = GaozhongItem()

        #获取学校名字
        try:
            school_name = []
            school_names = response.xpath("/html/body/div[6]/div[1]/div[@class='p_bor']/a/text()")
            for name in school_names:
                school_name.append(name.root.encode('utf-8'))
            haogaozhong["school_name"] = school_name
        except Exception as e:
            print(str(e))

        #获取在haogaozhong官方生成的URL
        try:
            school_html = []
            school_htmls = response.xpath("/html/body/div[6]/div[1]/div[@class='p_bor']/a/@href")
            for ht in school_htmls:
                school_html.append(self.url_join[0] + ht.root)
            haogaozhong["school_html"] = school_html
            #通过get_md5()生成每个URL自己独有的URL，可以防止URL重复爬取
            try:
                url_id = []
                if school_html:
                    for url in school_html:
                        url_id.append(get_md5(url))
                    haogaozhong["school_id"] = url_id
            except Exception as e:
                print(str(e))
        except Exception as e:
            print(str(e))

        #获取学校图片的url
        try:
            school_image_url = []
            # /html/body/div[6]/div[1]/div[3]/div[1]/p/a/img
            school_image_urls = response.xpath("/html/body/div[6]/div[1]/div[@class=' mar_t_30 overhidden']/div[@class='img_160 left mar_r_30']/p/a/img/@src")
            for tel in school_image_urls:
                school_image_url.append(tel.root)
            haogaozhong["school_image_url"] = school_image_url
        except Exception as e:
            print(str(e))

        # 获取学校所在的省份、市级、县级
        try:
            #@class=' mar_t_30 overhidden'
            school_province = []
            school_city = []
            school_town = []
            #/html/body/div[6]/div[1]/div[6]/div[2]/table/tbody/tr[1]/td[1]
            school_addresses = response.xpath("/html/body/div[6]/div[1]/div[@class=' mar_t_30 overhidden']/div[2]/table/tr[1]/td[1]/text()")
            for addresses in school_addresses:
                address = addresses.root.replace("&nbsp", " ")
                address = address.split()
                if len(address) == 3:
                    school_province.append(address[0].encode('utf-8'))
                    school_city.append(address[1].encode('utf-8'))
                    school_town.append(address[2].encode('utf-8'))
                else:
                    school_province.append(address[0].encode('utf-8'))
                    school_city.append(address[1].encode('utf-8'))
                    school_town.append(address[1].encode('utf-8'))
            haogaozhong["school_province"] = school_province
            haogaozhong["school_city"] = school_city
            haogaozhong["school_town"] = school_town
        except Exception as e:
            print(str(e))

        # 获取学校自己的URL
        try:
            #@class=' mar_t_30 overhidden'
            school_page = []
            #/html/body/div[6]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/a
            school_pages = response.xpath("/html/body/div[6]/div[1]/div[@class=' mar_t_30 overhidden']/div[2]/table/tr[1]/td[2]/a/@href")
            for page in school_pages:
                if page.root:
                    school_page.append(page.root)
                else:
                    school_page.append('no school web_url!')
            haogaozhong["school_page"] = school_page

        except Exception as e:
            print(str(e))

        # 获取学校类型
        try:
            school_type = []
            #/html/body/div[6]/div[1]/div[3]/div[2]/table/tbody/tr[2]/td[1]
            school_types = response.xpath("/html/body/div[6]/div[1]/div[@class=' mar_t_30 overhidden']/div[2]/table/tr[2]/td[1]/text()")
            for types in school_types:
                 type = types.root.split()
                 school_type.append(type[1].encode('utf-8'))
            haogaozhong["school_type"] = school_type
        except Exception as e:
            print(str(e))

        # 获取学校人气
        try:
            school_num = []
            #/html/body/div[6]/div[1]/div[3]/div[2]/table/tbody/tr[3]/td
            school_numbers = response.xpath("/html/body/div[6]/div[1]/div[@class=' mar_t_30 overhidden']/div[2]/table/tr[3]/td/text()")
            for nums in school_numbers:
                num = nums.root.replace("：", " ")
                num = num.split()[1]
                school_num.append(num)
            haogaozhong["school_num"] = school_num
        except Exception as e:
            print(str(e))

        # 获取学校办公电话
        try:
            school_tel = []
            #/html/body/div[6]/div[1]/div[3]/div[2]/table/tbody/tr[2]/td[2]
            school_telephones = response.xpath("/html/body/div[6]/div[1]/div[@class=' mar_t_30 overhidden']/div[2]/table/tr[2]/td[2]/text()")
            for telephones in school_telephones:
                tels = telephones.root.replace("：" , " ")
                tel = tels.split()
                if len(tel) == 2:
                    school_tel.append(tel[1])
                else:
                    school_tel.append('0')
            haogaozhong["school_tel"] = school_tel
        except Exception as e:
            print(str(e))

        yield haogaozhong

        # 获取下一页URL，并将其传回给parse()
        try:
            # //div[@id='pagenav']/ul/li[3]/a
            next_urls = []
            next_url = response.xpath("//div[@id='pagenav']/ul/li[3]/a/@href")
            if next_url:
                for i in next_url:
                    next_urls.append(self.start_urls[0] + i.root)
                    yield Request(url=next_urls[0], callback=self.parse)
        except Exception as e:
            print(str(e))

