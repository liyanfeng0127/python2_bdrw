import os
import urllib.parse
import urllib.request
import time
import re
import pymysql.cursors

def getAllOldData():
    '获取所有的数据'
    rUrl = 'http://baidu.lecai.com/lottery/draw/list/543'
    #1285862400 2010.10.1时间戳
    crtTime = time.time()
    oldTime = 1285862400
    timeList = []

    while True:
        if oldTime > crtTime:
            break
        else:
            oldTime += 3600 * 24
            dateList = list(time.localtime(oldTime))
            timeStr = str('%s-%s-%s'%(dateList[0],dateList[1],dateList[2]))
            timeList.append(timeStr)
    # ipList = getipList()

    for nowT in timeList:
        # exChangeIP(ipList)
        saveDataWithDate(nowT,rUrl)
        time.sleep(0.1)


def saveDataWithDate(date,url):
    newURL = url+"?d="+date
    req = urllib.request.Request(newURL, {})
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0')
    response = urllib.request.urlopen(newURL)
    html = response.read().decode('utf8')
    htmlStr = str(html).replace('\t','').replace('\n','').replace(' ','')


    qishuList = re.findall(r'\<tdclass\=\"td2\">\d{6}\<\/td\>',htmlStr)
    pointList =  re.findall(r'(\<spanclass\=\"ball\_1\"\>\d{2}\<\/span\>)',htmlStr)
    pointList2 =  re.findall(r'(\<spanclass\=\"ball\_1\"\>\d{2}\<\/span\>){20}',htmlStr)
    dataDic = {}
    for i in range(len(qishuList)):
        qishuStr = qishuList[i]
        onepointList = pointList[i*20:i*20+20]
        pList = re.findall(r'\d{2}',str(onepointList))
        pointID = (re.findall(r'\d{6}',qishuStr))[0]
        oneListStr = ''
        for p in pList:
            oneListStr += str(p + ',')
        oneListStr = oneListStr[:-1]
        dataDic[pointID] = {'str':oneListStr,'date':date}
    saveData(dataDic)



def saveData(dataDic):
    # 进行建表等操作
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='caipiaodata',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    # 创建表的操作
    cursor = connection.cursor()

    for (k,v) in dataDic.items():
        darr = str(v['date'])
        dstr = str(v['str'])
        print(k,darr,dstr)
        sql = str("INSERT INTO cptb(cpID,cpdate,str)VALUES('%s','%s','%s')"%(str(k),darr,str(dstr)))
        try:
            cursor.execute(sql)
            connection.commit()
            print('yes')
        except:
            connection.rollback()
            print('no')
    connection.close()

def creattb():
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='caipiaodata',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    # 创建表的操作
    cursor = connection.cursor()
    cursor.execute('drop table if exists cptb')
    sql = """create table cptb
    (
    id INTEGER AUTO_INCREMENT primary key,
    cpID CHAR (20) UNIQUE KEY  ,
    cpdate CHAR (200),
    str CHAR (100)
    )"""
    cursor.execute(sql)
    connection.close()


def reloadData():
    #首先找到最新的一组
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='caipiaodata',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    cursor.execute('select * from cptb where cpID > 0 order by cpID DESC limit 1')
    result = cursor.fetchall()[0]
    date = result['cpdate']

    timeList = []
    crtTime = time.time()
    timeArray = time.strptime(date,'%Y-%m-%d')
    timeStamp = int(time.mktime(timeArray))
    oldTime = timeStamp
    rUrl = 'http://baidu.lecai.com/lottery/draw/list/543'
    print('oldtime = '+str(oldTime)+'   newTime = '+str(crtTime))

    while True:
        if oldTime > crtTime:
            print('break')
            break
        else:
            dateList = list(time.localtime(oldTime))
            timeStr = str('%s-%s-%s' % (dateList[0], dateList[1], dateList[2]))
            timeList.append(timeStr)
            oldTime += 3600 * 24
    for nowT in timeList:
        # exChangeIP(ipList)
        saveDataWithDate(nowT,rUrl)
        time.sleep(0.1)



if __name__ == '__main__':
    # creattb()
    # getAllOldData()
    # saveData({})
    reloadData()
