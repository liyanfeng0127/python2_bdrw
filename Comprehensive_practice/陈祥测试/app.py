#coding:utf-8
import time
from download import link_crawler,Downloader
from mysql_table import SQLCache,SQLQueue,Seen,JobsCache
import re
def drop(table1,table2):
    table1.delete_all()
    table2.delete_all()

def extract_urls(html):
    webpage_regex = re.compile('<td[^>]+><a[^>]+href=["\'](http://jobs\.zhaopin.com/[^/"\']+\.htm)["\']',re.IGNORECASE)
    return webpage_regex.findall(html)

def data_crawler(downloader,queue,seen,datacache):

    while len(queue):
        url = queue.pop()
        if url not in seen:
            try:
                html = downloader(url)
            except Exception,e:
                print e
                continue
            else:
                seen.append(url)

            getDataFrom(html,datacache)

find ={
        'id':re.compile('<link rel="canonical"[^>]+.com/(.*)\.',re.IGNORECASE),
        'jobcompanyname':re.compile('<h1>(.*)</h1>[^<]*<h2>[^<]*<a[^>]+>(.*)</a>',re.IGNORECASE),
        'salary':re.compile('职位月薪[^<]*</span><strong>(.*元/月)',re.IGNORECASE),
       'workplace':re.compile('工作地点[^<]*</span><strong><a[^>]+>(.*)</a>'),
       'releasetime':re.compile('发布日期[^<]*</span><strong><span[^>]+>(.*)</span>'),
       'workexperience':re.compile('工作经验[^<]*</span><strong>(.*)</strong>'),
       'educationalrequirements':re.compile('最低学历[^<]*</span><strong>(.*)</strong>'),
       'recruitnumbers':re.compile('招聘人数[^<]*</span><strong>(.*)</strong>'),
       'jobcategory':re.compile('职位类别[^<]*</span><strong><a[^>]+>(.*)</a>'),
       'jobdescription':re.compile(r'SWSStringCutStart[^>]+>([.\s\S]*) <[^<]+SWSStringCutEnd',re.IGNORECASE)
       }

def getDataFrom(html,datacache):
    g = {}
    for key in find:
        g[key]=find[key].search(html).group(1)
    g['jobname']=g['jobcompanyname']
    g['companyname']=find['jobcompanyname'].search(html).group(2)
    jobdescription = [str.strip() for str in re.findall('>([^<>]*)<',g['jobdescription']) ]
    g['jobdescription'] = '\n'.join(jobdescription)
    datacache.append(id=g['id'],CompanyName=g['companyname'],JobName=g['jobname'],
                              Salary=g['salary'],ReleaseDate=g['releasetime'],WorkExperience=g['workexperience'],
                              RecruitingNumbers = g['recruitnumbers'],
                              WorkPlace=g['workplace'], EducationalRequirements=g['educationalrequirements'],
                              JobCategory=g['jobcategory'],JobDescription=g['jobdescription'])



if __name__ == '__main__':
    page_max = 90
    pages_url = ["http://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国&kw=嵌入式&p=%s"%str(i) for i in range(page_max)]
    D=Downloader() #下载HTML
    import requests

    sqlcache = SQLCache()
    sqlqueue = SQLQueue()
    jobscache = JobsCache()
    sqlseen = Seen()
    drop(sqlqueue, sqlseen)
    jobscache.delete_all()
    jobscache = JobsCache()

    urlsx = [extract_urls(D(url)) for url in pages_url]
    for urls in urlsx:
        for url in urls:
           sqlqueue.append(url)

    data_crawler(D,sqlqueue,sqlseen,jobscache)

    #sqlseen = Seen()
    #drop(sqlqueue, sqlseen)
    #jobscache.append('12','还上课时刻','嵌入式工程师','1000-30000','2017-3-19','三年经验', '深证','本科','IT','厉害的一比')
    #jobscache.append(id='',)
    #data_crawler(D,sqlseen,sqlseen,jobscache)
    #print len(urls),urls


'''
    start =int (time.time())
    seed_url='http://example.webscraping.com'
    #link_regex='/(index|view)'
    link_regex = '.*'
    #cache=mongo_cache.MongoCache()
    seed_url='http://www.baidu.com/s?wd=sex'
    seed_url='http://www.douban.com/subject'
    sqlcache = SQLCache()
    #SQLCache.drop()
    sqlqueue = SQLQueue()
    sqlseen = Seen()
    drop(sqlqueue,sqlseen)
    link_crawler(seed_url,link_regex,crawl_queue=sqlqueue,seen=sqlseen,cache={})
    end = int (time.time())
    print"It takes %s minutes %s seconds"%((end-start)/60,(end-start)%60)
'''