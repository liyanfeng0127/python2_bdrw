#-*-coding:utf8-*-

import sys
import string
import jieba
import jieba.posseg
import numpy as np
import pandas as pd
import re

reload(sys)
sys.setdefaultencoding('gbk')

def parsefile(inputfile , inputdict):
    dict_list = open(inputdict, 'r').read().split(' \n')
    file_list = pd.read_csv(inputfile )
    return file_list,dict_list

def tici(file_list,dict_list,path):
    jieba.load_userdict(path)
    for i in range(1, 50):
        data2 = []
        words = jieba.posseg.cut(file_list.iloc[i][0])
        for word, flag in words:
            if word in data2:
                continue
            else:
                data2.append(word.encode('gbk'))
# data2现在是ASCII表示
        for param in dict_list:
            if param in data2:
                data.append(param + '\t')
                # data.append(param + ',')
                #注释掉的部分是读CSV格式的编写
        if data2:
            data.append('\n')
        del data2
    print data
    return data

def filewrite(outputfile ,data):
    fw = open(outputfile , 'wt')
    fw.writelines(data)
    fw.close()

if __name__ == '__main__':
    inputfile = u'G://PyCharm//data//预处理_岗位描述.csv'
    inputdict = u"G://PyCharm//data//词典22.txt"
    # inputdict = u"G://PyCharm//data//嵌入式词典2.txt"
    outputfile = 'new_dict.xlsx'
    # outputfile = 'new_dict.csv'
    path = "G:/PyCharm/data/SogouLabDic.txt"
    file_list, dict_list = parsefile(inputfile , inputdict)
    data = []
    data = tici(file_list , dict_list ,path)
    result = filewrite(outputfile,data)

