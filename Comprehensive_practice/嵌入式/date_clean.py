#-*-coding:utf8-*-

from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import sys
from sqlalchemy import create_engine
import pymongo
import pandas as pd
import numpy as np
from scipy.interpolate import lagrange


reload(sys)
sys.setdefaultencoding('utf-8')

datafile = './dajiewang.csv'
outputfile = './data_clean.csv'

data = pd.read_csv(datafile , encoding='utf-8')

for i in range(len(data)):
    if (data['公司类型'].isnull())[i]:
        data['公司类型'][i] = '其他'
    if (data['发布时间'].isnull())[i]:
        data[i] = data[i + 1]
#拉格朗日插补法
# def ployinterp_column(s , n , k=5):
#     y = s[list(range(n-k , n)) + list(range(n+1 , n+1+k))]
#     y = y[y.notnull()]
#     return lagrange(y.index , list(y))(n)

#逐个元素差值
# for i in data.columns:
#     for j in range(len(data)):
#         if (data[i].isnull())[j]:
#             data[i][j] = ployinterp_column(data[i] , j)

data.to_csv(outputfile , header=None , index=False)

