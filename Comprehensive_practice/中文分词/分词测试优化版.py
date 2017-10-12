#-*-coding:utf8-*-

import jieba
import jieba.posseg
import jieba.analyse
import pandas as pd
import nltk
import time
import sys
import multiprocessing

reload(sys)
sys.setdefaultencoding('utf-8')
def openfile(path):
    data = pd.read_csv(path)
    return data


#利用结巴分词处理文本关键词‘eng’
def parse_all(data , flaglists ,path):
    a = len(data)
    new_list = []
    jieba.load_userdict(path)
    for name in flaglists:
        # list_'{}'.format(name) = []
        file = open(u'词标_{}.txt'.format(name) , 'wt')
        for i in range(1 , a):
            words = jieba.posseg.cut(data.iloc[i][0])
            for word, flag in words:
                if flag == '{}'.format(name):
                    new_list.append(word)
        fdist = nltk.FreqDist(new_list)
        del new_list[:]
        for keys, values in sorted(fdist.items(), key=lambda x: x[1]):
            file.writelines(keys + '  ' + str(values) + '  ' + '{}'.format(name) + u'\n')
        file.close()

if __name__ == '__main__':
    t1 = time.time()
    path1 = u'G://PyCharm//data//预处理_岗位描述.csv'  # 原始数据路径
    path2 = "G:/PyCharm/data/SogouLabDic.txt"  # 外部语料库
    flagwords = ['eng', 'nz', 'l' , 'n']  # 词性标注列表
    data = openfile(path= path1)
    f = open('youhuaxiaolv.csv' , 'a')
    ceshi = multiprocessing.Process(target=parse_all ,args=(data , flagwords , path2))
    ceshi.start()
    ceshi.join()
    t2 = time.time()
    t3 = t2 - t1
    f.writelines(u"第2测试，利用multiprocessing后，时间差：{} ,\n".format(t3))
    f.close()