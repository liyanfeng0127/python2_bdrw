#-*-coding:utf8-*-
__author__ = 'liyanfeng'

import sys
import os
from scrapy.cmdline import execute

reload(sys)
sys.setdefaultencoding('utf-8')

# print os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  #获取文件path
execute(["scrapy", "crawl", "wanfangdata"])   #cmd指令传输



