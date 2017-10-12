# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from doubanmovie.items import DoubanmovieItem

class Douban(CrawlSpider):
    name = "douban"
    redis_key = 'douban:start_urls'
    start_urls = ['https://movie.douban.com/top250']

    url = 'https://movie.douban.com/top250'

    def parse(self,response):
        #print response.body
        item = DoubanmovieItem()
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMoive in Movies:
            title = eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle = ''
            for each in title:
                #print each
                fullTitle += each
            #print fullTitle
            movieInfo = eachMoive.xpath('div[@class="bd"]/p/text()').extract()
            star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span/text()').extract()[0]
            quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            #quote可能为空，因此需要先进行判断
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = fullTitle
            item['movieInfo'] = ';'.join(movieInfo)
            item['star'] = star
            item['quote'] = quote
            #print item
            #yield item
        nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        #第10页是最后一页，没有下一页的链接
        if nextLink:
            nextLink = nextLink[0]
            print nextLink
            yield Request(self.url + nextLink,callback=self.parse)
