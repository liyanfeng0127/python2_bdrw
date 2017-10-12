#-*-coding:utf8-*-

import sys
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

def csv_to_xls(path1 , path2):
    readcsv = pd.read_csv(path1).replace(' ' , '\t')
    print readcsv
    # a = len(readcsv)
    # print a
    # for i in range(1 , 10):
    #     if readcsv.iloc[i]
    #     read = readcsv.iloc[i]
    #     print read
    # fw = open(path2, 'wt')
    # fw.writelines(read)
    # fw.close()

def txt_to_xls(path1 , path2):
    readtxt = open(path1 , 'rb').read().encode('utf-8').replace('\n' , '')
    readtxt = readtxt.replace(',' , '\t')
    a = len(readtxt)
    print readtxt
    fw = open(path2, 'wt')
    fw.writelines(readtxt)
    fw.close()


if __name__ == '__main__':
    path = u'G://PyCharm//data//分栏岗位.xls'
    path1 =  u'分栏岗位.csv'
    path2 = '12.txt'
    # result = csv_to_xls(path1 , path)
    result = txt_to_xls(path2 , path)

