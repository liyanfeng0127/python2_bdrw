# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst


def add_data(value):
    return value + "data"


class WanfangspiderTxtItem(scrapy.Item):
    all_urls = scrapy.Field()

class WanfangspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(
        # input_processor = MapCompose(add_data)
        # input_processor=MapCompose(lambda x : x + "wanfang", add_data)
        # output_processor = TakeFirst()
    )

    # urllist = scrapy.Field()
    url_content = scrapy.Field()
    #通过哈希hash的md5函数，生成唯一且长度固定的id值
    url_object_id = scrapy.Field()
    spider_keyword = scrapy.Field()
    description = scrapy.Field()
    spider_url = scrapy.Field()
    all_urls = scrapy.Field()
    image_url = scrapy.Field()
    image_url_path = scrapy.Field()
    #wangfangdata["url_images"] = [url_images]

    def get_insert_sql(self):
        insert_mysql = """
                        insert into wanfangdata(url_object_id, spider_url, title, url_content, spider_keyword, image_url) 
                        VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE url_object_id=VALUES(url_object_id)
                    """
        params = (str(self["url_object_id"]), str(self["spider_url"]), str(self["title"]),
                str(self["url_content"]), str(self["spider_keyword"]), str(self["image_url"]))

        return insert_mysql, params

