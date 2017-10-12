# -*- coding: utf-8 -*-
from lxml import etree
import requests
import sys
from multiprocessing.dummy import Pool as ThreadPool

reload(sys)
sys.setdefaultencoding('utf-8')

def towrite(parm):
    # f.writelines(u'职位名称：' + str(parm['recruit_jobs']) + '\n')
    # f.writelines(u'公司名称：' + str(parm['recruit_company']) + '\n')
    # f.writelines(u'公司网站：' + str(parm['recruit_company_net']) + '\n')
    #
    # f.writelines(u'工作地点：' + str(parm['recruit_workplace']) + '\n')
    # f.writelines(u'发布时间：' + str(parm['recruit_time']) + '\n')
    # f.writelines(u'岗位职责：' + str(parm['recruit_responsibilities']) + '\n\n')
    pass

def spider(url):
    html = requests.get(url).content
    xinzhi=[]
    import re
    xinzhi=re.findall('<td class="zwyx">(.*)</td>',html)
    print xinzhi
    recruit_responsibilities = re.findall( '<li class="newlist_deatil_last">(.*)</li>', html , re.S)
    item = {}
    # print recruit
    # recruit = selector.xpath('//div[@id="newlist_list_content_table"]/table[@class="newlist"]/tbody/tr/td[@class="zwmc"]/div/a/text()')
    for each in recruit:
        # recruit_jobs = each.xpath('/tbody/tr/td[@class="zwmc"]/div/a')[0]
        # recruit_jobs = list(recruit_jobs.xpath('string(.)'))
        # recruit_jobs = ''.join(recruit_jobs)
        # recruit_company_net = each.xpath('/tbody/tr/td[@class="gsmc"]/a/@href')
        # print recruit_company_net
        # print recruit_company_net
        # recruit_company = each.xpath('tbody/tr/td[@class="gsmc"]/a/text()')
        # recruit_salary = each.xpath('/tbody/tr/td[@class="zwyx"]/text()')
        # recruit_workplace = each.xpath('/tbody/tr/td[@class="gzdd"]/text()')
        # recruit_time = each.xpath('/tbody/tr/td[@class="gxsj"]/span/text()')
        # recruit_responsibilities = each.xpath('tbody/tr[@class="newlist_tr_detail"]/td[@class="gxsj"]/td/div/div/ul/li[@class="newlist_deatil_last"]/text()')
        # print recruit_responsibilities
        # recruit_responsibilities = list(recruit_responsibilities.xpath('string(.)'))
        # recruit_responsibilities = ''.join(recruit_responsibilities)
        # item['recruit_jobs'] = recruit_jobs
        # item['recruit_company_net'] = recruit_company_net
        # item['recruit_company'] = recruit_company
        # item['recruit_salary'] = recruit_salary
        # item['recruit_workplace'] = recruit_workplace
        # item['recruit_time'] = recruit_time
        # item['recruit_responsibilities'] = recruit_responsibilities
        towrite(item)



    # nextlink = selector.xpath('//html/body/div[@class="main"]/div[@class="search_newlist_main"]/div[@class="newlist_main"]/form/div[@class="clearfix"]/div[@class="newlist_wrap fl"]/div[@class="pagesDown"]/ul/li[@class="pagesDown-pos"]/a/@href')
    # if nextlink:
    #     nextlink = nextlink[0]
    #     spider(nextlink)


if __name__ == '__main__':

    # pool = ThreadPool(4)
    f = open('Embedded_recruitment.csv','a')
    page = []
    for i in range(1, 5):
        newpage = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&jl=北京&kw=嵌入式&sm=0&isfilter=1&fl=530&isadv=0&sb=1&sg=8de28363eb064a2b8ab40da3111bbceb&p=' + str(i)
        page.append(newpage)
    result = map(spider,page)
    # pool.close()
    # pool.join()
    f.close()