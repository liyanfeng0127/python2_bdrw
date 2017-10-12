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
# stopwords = ['、', '（', '）', '， ', '。', ':', '“', '”', '\n\u3000', '\u3000', '的', '‘', '’', '了', '.', '如', '有', '对'， '?', '；']  # 停用词
stopwords = [':', '?', '.']
file = open('old_dict1.txt' , 'r').read().encode('utf-8')
f = open('new_list.txt' , 'a')
fredist = nltk.FreqDist(file.split(' '))
for local_keys in fredist.keys():# 所有词频合并。如果存在，词频相加；否则添加
    if local_keys in stopwords: # 检查是否为停用词
        continue
    if local_keys in dictionary:# 检查当前词频是否在字典中存在
        dictionary[local_keys] = dictionary[local_keys] + fredist[local_keys]# 如果存在，将词频累加，并更新字典值
    else:# 将当前词频添加到字典中
        dictionary[local_keys] = fredist[local_keys]
strs = str(sorted(dictionary.items(), key=lambda x: x[1]))
# f.writelines(strs)
# f.close()