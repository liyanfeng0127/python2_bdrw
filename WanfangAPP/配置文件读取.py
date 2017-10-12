#-*-coding:utf8-*-

import sys
import time
import pandas as pd
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
from sqlalchemy import create_engine
import pymongo


reload(sys)
sys.setdefaultencoding('utf-8')

def readcsv(path1):
    urllist = []
    with open(path1) as af:
        try:
            initdata = pd.read_csv(af)
            for i in range(1, len(initdata)):
                urllist.append(initdata.iloc[i][0])
            return urllist
        finally:
            af.close()

def readtxt(path2):
    urllist = []
    with open(path2) as af:
        try:
            for initurl in af.readlines():
                urllist.append(initurl)
            return urllist
        finally:
            af.close()

def parseurl(urllist):
    if urllist:
        for initurl in urllist:
            html = requests.get(initurl).content   #HTML解析文本


    else:
        print "read the file is fault!"





if __name__ == '__main__':
    t1 = time.time()
    path1 = u'G://PyCharm//data//配置文件.csv'  # 原始数据路径
    path2 = u'G://PyCharm//data//配置文件.txt'  # 原始数据路径
    length = len(initdata)
    for
        seconddata = initdata.iloc[]

