#-*-coding:utf8-*-

from lxml import etree
import requests
import sys
import re
import pymongo
from multiprocessing.dummy import Pool as ThreadPool
from scrapy.http import Request
import time

reload(sys)
sys.setdefaultencoding('utf-8')

import lxml
lxml.


#穿入url列表，可以获取累加式的新url列表
def deep_pasre_url(start_url, all_number):
    html = requests.get(start_url,{})
    qishu = re.findall(r'<td>([\d]{6})<\/td>', str(html))
    if len(all_munber) :
        if qishu[0] in all_number:
            time.sleep(0.1)
            deep_pasre_url(start_url, all_number)
        else:
            all_number.append(qishu[0])
            time.sleep(299)
            deep_pasre_url(start_url, all_number)
            return all_number
    else:



def return_data(all_munber):
    with open("fucai.txt", 'w') as af:
        for fucai_data in all_munber:
            af.writelines(fucai_data + '\n')
    af.close()

def return_all_data(all_number):
    with open("fucai.txt", 'w+') as af:
        for fucai_data in all_munber:
            af.writelines(fucai_data + '\n')
    af.close()

if __name__ == '__main__':
    second_url = 'http://www.bwlc.gov.cn/bulletin/prevkeno.html'
    all_munber = ['834276']
    url_content = deep_pasre_url(second_url, all_munber)
    print url_content






