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

# def beutf8(dict):
#     for keys in dict:
#         key = keys.encode('utf-8')
#         return key

dictionary = {}  # 空字典 用于保存最终的词频
new_list = []
# stopwords = ['、', '（', '）', '， ', '。', ':', '“', '”', '\n\u3000', '\u3000', '的', '‘', '’', '了', '.', '如', '有', '对'， '?', '；']  # 停用词
stopwords = [':', '?', '.', ' ', '']
file = open('jieba_cut.txt' , 'r').read()
f = open('cishu_cipin.txt' , 'wt')#"wt" 只能写文件，如果文件不存在则创建；如果文件已存在，先清空，再打开文件
# f.truncate()清空文件内容
for words in file:
    if words in stopwords:
        continue
    if words in dictionary:
        dictionary[words] += 1
    else:
        dictionary[words] = 1
fredist = nltk.FreqDist(file.split(' '))
# for list1 in fredist.keys():
#     code_list = list1.encode('utf-8')
for keys , values in sorted(dictionary.items() ,key=lambda x :x[1]):
    f.writelines(keys.decode('utf-8' , 'ignore').encode('utf-8') + str(values) + '\n' )
# f.writelines(str(list1.encode('utf-8')) for list1 in fredist.keys())
f.close()
# for keys in dictionary:
#     key = keys.encode('utf-8')
#     value = dictionary[keys]
    # print key
# print beutf8(dictionary)
# for local_keys in fredist.keys():# 所有词频合并。如果存在，词频相加；否则添加
#     if local_keys in stopwords: # 检查是否为停用词
#         continue
#     if local_keys in dictionary:# 检查当前词频是否在字典中存在
#         dictionary[local_keys] = dictionary[local_keys] + fredist[local_keys]# 如果存在，将词频累加，并更新字典值
#     else:# 将当前词频添加到字典中
#         dictionary[local_keys] = fredist[local_keys]
# strs = str(sorted(dictionary.items(), key=lambda x: x[1]))
