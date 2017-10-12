# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
from scrapy.pipelines.images import ImagesPipeline
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
#异步端口
from twisted.enterprise import adbapi
from gaozhong.ultil.command import get_md5


class WanfangspiderPipeline(object):
    def process_item(self, item, spider):
        #进行数据存储，可以放到数据库中
        return item

class TxtDataPipeline(object):
    def __init__(self):
        self.file_txt = open('wanfangdata.txt', 'wt')

    def process_item(self, item, spider):
        strlist = item["all_urls"]
        self.file_txt.writelines(u"爬取过的所有URL" + '\n')
        for i in range(len(strlist)):
            self.file_txt.writelines(strlist[i] + '\n')

    def spider_closed(self, spider):
        self.file_txt.close()


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

    def do_insert(self, cursor, item):
        #执行具体逻辑插入
        # insert_mysql = """
        #                        insert into wanfangdata(url_object_id, spider_url, title, url_content, spider_keyword, image_url)
        #                        VALUES (%s, %s, %s, %s, %s, %s)
        #                    """
        # # item["description"]
        # cursor.execute(insert_mysql, (str(item["url_object_id"]), str(item["spider_url"]), str(item["title"]),
        #                               str(item["url_content"]), str(item["spider_keyword"]), str(item["image_url"])))
        insert_mysql, params = item.get_insert_sql()
        cursor.execute(insert_mysql,params)

class Mysqlpipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '1234', 'wanfangdata', charset= "utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if item.__class__.__name__ == "WanfangspiderItem":
            insert_mysql = """
                insert into wanfangdata(url_object_id, title, url_content, keywords, description, spider_url, image_url) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            self.cursor.execute(insert_mysql, (item["url_object_id"], item["title"], item["url_content"],
                            item["keywords"], item["description"], item["spider_url"], item["image_url"]))
            self.conn.commit()

class JsonExporterPipelines(object):
    #调用scrapy自带的Json_Exporter函数导出json文件
    def __init__(self):
        self.file = open("wanfangdata.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

#保存JS格式文件
class JsonWithEncodingPipeline(object):
    #自定义json文件导出
    def __init__(self):
        self.file = codecs.open("wanfangdata.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


#设置图片的pipeline
class WanfangImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for keys, values in results:
            images_file_path = values["path"]
        item["image_url_path"] = images_file_path

        return item

