#-*-coding:utf8-*-

import pandas as pd
from apriori import *
import sys
import Apriori

reload(sys)
sys.setdefaultencoding('utf-8')

inputfile ='G://PyCharm//data//menu_orders.xls'
outputfile = 'apriori_rules.csv' #结果文件
data = pd.read_excel(inputfile)

print(u'\n转换原始数据至0-1矩阵。。。')
ct = lambda x :pd.Series(1 , index=x[pd.notnull(x)])
b = map(ct , data.as_matrix())
data = pd.DataFrame(list(b)).fillna(0)
print(u'\n转换完毕。')
del b

support = 0.2 #最小支持度
confidence = 0.5 #最小置信度
ms = '---'

Apriori.find_rule(data, support, confidence, ms).to_csv(outputfile) #保存结果
