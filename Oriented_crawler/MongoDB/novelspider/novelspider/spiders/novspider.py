#-*-coding:utf8-*-

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from novelspider.items import NovelspiderItem
#Pycharm在这里会提示找不到novelspider,这是因为这个爬虫是放在program这个大的文件夹下的
#这属于误报，程序可以正常运行。

class novSpider(CrawlSpider):
    name = "novspider"
    redis_key = 'nvospider:start_urls'
    start_urls = ['http://www.daomubiji.com/']

    def parse(self,response):
        selector = Selector(response)
        #/html/body/div[6]/div/center/table/tbody/tr[2]/td[1]/a
        table = selector.xpath('//body/div[@class="bg"]')
        print table
        for each in table:
            bookName = each.xpath('/div/center/table/tbody/tr/td/center/h2/text()').extract()[0]
            content = each.xpath('div[@class="bg"]/div[@class="content"]').extract()
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
                yield item