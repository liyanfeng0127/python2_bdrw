# -*- coding: utf-8 -*-


import codecs
from scrapy.pipelines.images import ImagesPipeline
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
#异步端口
from twisted.enterprise import adbapi

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GaozhongPipeline(object):
    def process_item(self, item, spider):
        return item

#异步存入MySQL数据库
class MysqlTwistedpipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
             )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将MySQL插入变成异步
        query = self.dbpool.runInteraction(self.do_insert, item)
    #     query.addErrorback(self.handle_error)

    # def handle_error(self, failure):
    #     #处理异步插入的异常
    #     print failure
#,  school_image_url, school_province, school_city, school_town, school_page, school_type, school_num, school_tel

    def do_insert(self, cursor, item):
        try:
            if item.get('school_name'):
                insert_mysql = """
                                    insert into haogaozhong(school_name, school_html, school_id,  school_image_url, school_province, school_city, school_town, school_page, school_type, school_num, school_tel)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """
                for i in range(len(item['school_name'])):
                    cursor.execute(insert_mysql, (str(item['school_name'][i]), str(item['school_html'][i]), str(item['school_id'][i]), str(item['school_image_url'][i]), str(item['school_province'][i]),
                                                  str(item['school_city'][i]), str(item['school_town'][i]), str(item['school_page'][i]), str(item['school_type'][i]), str(item['school_num'][i]), str(item['school_tel'][i])))
        except Exception as e:
            print(str(e))

