#-*-coding:utf8-*-

import sys
import jieba
import jieba.posseg
import jieba.analyse
import pandas as pd
import codecs
import nltk


reload(sys)
sys.setdefaultencoding('utf-8')

dictionary = {}  # 空字典 用于保存最终的词频
new_list = []
file = open(u'结巴_cut.txt' , 'r').read()
f = open(u'词组_词数.txt' , 'wt')
fredist = nltk.FreqDist(file.split(' '))
# for keys,values in fredist.items():
#     print keys + str(values)
for keys,values in sorted(fredist.items() ,key=lambda x :x[1]):
    f.writelines(keys + str(values) + u'\n')
f.close()