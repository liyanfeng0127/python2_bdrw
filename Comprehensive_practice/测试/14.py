#-*-coding:utf8-*-

import sys
import string
reload(sys)
sys.setdefaultencoding('utf-8')

import jieba
import jieba.posseg as pseg
import os
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from numpy import *
import pandas as pd

# sys.path.append("C:\Users\Administrator\Desktop\9.17")#默认路径

inputfile = u'G://PyCharm//data//预处理_岗位描述.csv'
fr_list = pd.read_csv(inputfile)
a = len(fr_list)
data = []
jieba.load_userdict("G:/PyCharm/data/SogouLabDic.txt")
for i in range(1 , a):
    data.append(" ".join(jieba.cut(fr_list.iloc[i][0])))

#将得到的词语转换为词频矩阵
freWord = CountVectorizer()

#统计每个词语的tf-idf权值
transformer = TfidfTransformer()
#计算出tf-idf(第一个fit_transform),并将其转换为tf-idf矩阵(第二个fit_transformer)
tfidf = transformer.fit_transform(freWord.fit_transform(data))

#获取词袋模型中的所有词语
word = freWord.get_feature_names()

#得到权重
weight = tfidf.toarray()
tfidfDict = {}
for i in range(len(weight)):
    for j in range(len(word)):
        getWord = word[j]
        getValue = weight[i][j]
        if getValue != 0:
            if tfidfDict.has_key(getWord):
                tfidfDict[getWord] += string.atof(getValue)
            else:
                tfidfDict.update({getWord:getValue})
sorted_tfidf = sorted(tfidfDict.iteritems(),key = lambda d:d[1],reverse = True)
fw = open(u'14_TFIDF初步.txt','wt')
for i in sorted_tfidf:
    fw.write(i[0] + '\t' + str(i[1]) +'\n')
fw.close()

