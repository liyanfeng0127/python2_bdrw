#-*-coding:utf8-*-

from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import sys
from sqlalchemy import create_engine
import pymongo


# engine = create_engine("mysql://root:1234@localhost/scraping?charset=utf8")
# df1.to_sql('news_data',engine,if_exists='append')
reload(sys)
sys.setdefaultencoding('utf-8')





# connection = pymongo.MongoClient()
# tdb = connection.shijian
# post_info = tdb.test
#
# def InsertOne(one):
#     post_info.insert(one)

def beutf8(room):
    for a in room:
        room1 = a.encode('utf-8')
        return room1

def towrite(parm):
    # f.writelines("工作名称,公司名称,公司地址,发布时间,公司类型,公司规模,所属行业,工作类型,招聘人数,工作描述")
    strlist = [str(parm['JobName']),str(parm['Companyname']),str(parm['JobAdr']),
               str(parm['JobTime']),str(parm['Companytype']),str(parm['Companyscale']),
               str(parm['HiringNum']),str(parm['Jobdescription'])]
    strs=','.join(strlist)
    f.writelines(strs + '\n')
    '''
    f.writelines(u'工作名称：' + str(parm['JobName']) + '\n')
    f.writelines(u'公司名称：' + str(parm['Companyname']) + '\n')
    f.writelines(u'公司地址：' + str(parm['JobAdr']) + '\n')
    f.writelines(u'发布时间：' + str(parm['JobTime']) + '\n')
    f.writelines(u'公司类型：' + str(parm['Companytype']) + '\n')
    f.writelines(u'公司规模：' + str(parm['Companyscale']) + '\n')
    f.writelines(u'所属行业：' + str(parm['IndustrySubordinate']) + '\n')
    f.writelines(u'工作类型：' + str(parm['Jobcategory']) + '\n')
    f.writelines(u'招聘人数：' + str(parm['HiringNum']) + '\n')
    f.writelines(str(parm['Jobdescription']) + '\n')
    '''


def spider(url):
    html = requests.get(url).content
    selector = etree.HTML(html.decode('utf-8'))
    recruit = selector.xpath('//html/body/div[@class="wrapper"]/div[3]/div[1]/div/div[2]/ul/li')
    item = {}
    for each in recruit:
        Companyname = each.xpath('div[2]/p[@class="searchResultCompanyname"]/span/text()')[0]
        Jobdescription = each.xpath('div[2]/p[@class="searchResultJobdescription"]')[0]
        Jobdescription = list(Jobdescription.xpath('string(.)'))
        Jobdescription = ''.join(Jobdescription)
        Jobdescription1 = Jobdescription.replace(' ' , '').strip()
        JobName = each.xpath('div[2]/p[@class="searchResultJobName"]/a/text()')[0]
        JobAdr = each.xpath('div[2]/p[@class="searchResultJobAdrNum"]/span[1]/span/em/text()')[0]
        JobTime = each.xpath('div[2]/p[@class="searchResultJobAdrNum"]/span[2]/span/em/text()')[0]
        Companytype = each.xpath('div[2]/p[@class="searchResultCompanyInfodetailed"]/span[1]/span/em/text()')
        Companytype1 = beutf8(Companytype)
        Companyscale = each.xpath('div[2]/p[@class="searchResultCompanyInfodetailed"]/span[2]/span/em/text()')[0]
        # IndustrySubordinate = each.xpath('div[2]/p[@class="searchResultCompanyInfodetailed"]/span[3]/span/em/text()')[0]
        # Jobcategory = each.xpath('div[2]/p[@class="searchResultCompanyInfodetailed"]/span[4]/span/em/text()')
        # Jobcategory1 = beutf8(Jobcategory)
        # Jobcategory1 = ','.join(Jobcategory1)
        HiringNum = each.xpath('div[2]/p[@class="searchResultCompanyInfodetailed"]/span[5]/span/em/text()')[0]
        item['Companyname'] = Companyname
        item['Jobdescription'] = Jobdescription1
        item['JobName'] = JobName
        item['JobAdr'] = JobAdr
        item['JobTime'] = JobTime
        item['Companytype'] = Companytype1
        item['Companyscale'] = Companyscale
        # item['IndustrySubordinate'] = IndustrySubordinate
        # item['Jobcategory'] = Jobcategory
        item['HiringNum'] = HiringNum
        towrite(item)
    # #爬取的下一页网址带有汉字，但是老是显示16进制，所以无法递归
    # nextlink = selector.xpath('//ul[@id="page"]/li[11]/a/@href')
    # nextlink = str(nextlink).encode('utf-8')
    # if nextlink:
    #     nextlink = nextlink[0]
    #     spider(nextlink)
    # InsertOne(item)




if __name__ == '__main__':
    f = open('dajiewang3.csv', 'wt')
    f.writelines("工作名称,公司名称,公司地址,发布时间,公司类型,公司规模,招聘人数,工作描述" + '\n')
    pool = ThreadPool(4)
    page = []
    for i in range(1,15):
        newpage = 'http://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_嵌入式_' + str(i) + '_0'
        page.append(newpage)
    results = pool.map(spider, page)
    pool.close()
    pool.join()
    f.close()