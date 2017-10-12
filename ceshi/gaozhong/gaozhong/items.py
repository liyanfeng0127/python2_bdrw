# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GaozhongItem(scrapy.Item):
    #建立所需项目的item
    school_name = scrapy.Field()
    school_html = scrapy.Field()
    school_id = scrapy.Field()
    school_image_url = scrapy.Field()
    school_province = scrapy.Field()
    school_city = scrapy.Field()
    school_town = scrapy.Field()
    school_page = scrapy.Field()
    school_type = scrapy.Field()
    school_num = scrapy.Field()
    school_tel = scrapy.Field()


