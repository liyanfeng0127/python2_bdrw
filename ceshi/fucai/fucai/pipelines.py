# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FucaiPipeline(object):
    def process_item(self, item, spider):
        return item['name']

class FucaiTxtPipeline(object):
    def __init__(self):
        self.file_txt = open("fucai.txt", 'wt')

    def process_item(self, item, spider):
        strlist = item["name"]
        self.file_txt.writelines(u"爬取过的所有数字" + '\n')
        for i in range(len(strlist)):
            self.file_txt.writelines(strlist[i] + '\n')

    def spider_closed(self, spider):
        self.file_txt.close()
