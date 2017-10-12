#-*-coding:utf8-*-

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.http import Request
from novelspider.items import NovelspiderItem
import re

class novSpider(RedisSpider):
    name = "novspider"
    redis_key = 'nvospider:start_urls'
    start_urls = ['http://www.daomubiji.com/qi-xing-lu-wang-01.html']

    def parse(self,response):
        selector = Selector(response)
        table = selector.xpath('//body')
        for each in table:
            bookName = each.xpath('div[@class="bg"]/h1/text()').extract()[0]
            content = each.xpath('div[@class="bg"]/div[@class="content"]').extract()
            for eachcontent in content:
                Content = eachcontent.xpath('p/text()').extract()
            print Content
            url = each.xpath('tr/td/a/@href').extract()
            for i in range(len(url)):
                item = NovelspiderItem()  #为了防止后一个数据覆盖前一个数据，需要在每个循环里都实例化一个NovelspiderItem
                item['bookName'] = bookName
                item['chapterURL'] = url[i]
                # try可以用于检测错误，出现错误以后就会运行except里面的内容。
                try:
                    item['bookTitle'] = content[i].split(' ')[0]
                    item['chapterNum'] = content[i].split(' ')[1]
                except Exception,e:
                    continue

                try:
                    item['chapterName'] = content[i].split(' ')[2]
                except Exception,e:
                    item['chapterName'] = content[i].split(' ')[1][-3:]
                yield Request(url[i], callback='parseContent', meta={'item':item})

    def parseContent(self, response):
        selector = Selector(response)
        item = response.meta['item']
        html = selector.xpath('//div[@class="content"]').extract()[0]
        textField = re.search('<div style="clear:both"></div>(.*?)<div', html,re.S).group(1)
        text = re.findall('<p>(.*?)</p>',textField,re.S)
        fulltext = ''
        for each in text:
            fulltext += each
        item['text'] = fulltext
        yield item