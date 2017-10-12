
import pymysql.cursors
import urllib.request
import urllib.parse
import re
import time




def getNewDatafrombaidu():
    url = 'http://baidu.lecai.com/lottery/draw/view/543'
    req = urllib.request.Request(url, {})
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0')
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf8')
    htmlStr = str(html).replace('\t', '').replace('\n', '').replace(' ', '')

    qishuList = re.findall(r'latest_draw_phase\=\'\d{6}',htmlStr)
    qishuStr = qishuList[0]
    pointID = (re.findall(r'\d{6}', qishuStr))[0]
    reStr = str('latest_draw_result={"red"\:\["\d{2}","\d{2}","\d{2}","\d{2}","\d{2}","\d{2}","\d{2}","\d{2}","\d{2}","\d{2}"')
    pointList = re.findall(reStr,htmlStr)
    pointList = re.findall(r"\d{2}",str(pointList))
    # pointArr = re.findall(r'\d{2}',pointList[0])
    # print(pointID+str(pointList))


    oneListStr = ''
    for p in pointList:
        oneListStr += str(p + ',')
    oneListStr = oneListStr[:-1]
    return {pointID:oneListStr};


def getNewDataFromfucai():
    url = 'http://www.bwlc.gov.cn/bulletin/prevkeno.html'
    req = urllib.request.Request(url, {})
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0')
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf8')
    htmlStr = str(html).replace('\t', '').replace('\n', '').replace(' ', '')

    qishuList = re.findall(r'<td>\d{6}<\/td>', htmlStr)
    qishuStr = qishuList[0]
    pointID = (re.findall(r'\d{6}', qishuStr))[0]
    reStr = str('<td>\d{2},\d{2},')
    pointList = re.match(reStr, htmlStr)
    print(pointList)
    pointList = re.findall(r"\d{2}", str(pointList))
    print(pointID + '++++++++++++' + str(pointList))
    # pointArr = re.findall(r'\d{2}',pointList[0])
    # print(pointID+str(pointList))


    oneListStr = ''
    for p in pointList:
        oneListStr += str(p + ',')
    oneListStr = oneListStr[:-1]
    return {pointID: oneListStr};

def calculBest(newDic,oldDatas):
    #先从8个重复的字符开始计算
    cfs = 10
    resArr = []
    pointStr = list(newDic.values())[0]
    newDicId = list(newDic.keys())[0]
    print(pointStr + '+++++' +newDicId)

    while (cfs > 3):
        #如果找到了有相似的数据的话就直接跳出不需要进行-1
        for i in range(11-cfs):
            ppStr = pointStr[i*3:i*3+cfs*3]
            print(ppStr)
            #开始进行匹配
            for old in oldDatas:
                #在数据库中有最新数据的时候需要打开
                # if old['cpID'] == newDicId:
                #     print("有相同的值")
                #     continue;
                dataStr = str(old['str'])
                if ppStr in dataStr:
                    resArr.append({'pp': ppStr, 'data': old})
        if len(resArr) > 0:
            break;
        else:
            cfs -= 1
    print(resArr)

    nextDatas = []

    for res in resArr:
        nextID = str(int(res['data']['cpID']) + 1)
        sql  = str('select * from cptb WHERE cpID = %s'%(nextID))
        cursor.execute(sql)
        nextData = cursor.fetchall()
        nextDatas.append(nextData[0])

    #开始分析
    print(nextDatas)
    if len(nextDatas) >= 1:
        pstr = str(nextDatas[0]['str'])
        points = list(pstr.split(',',maxsplit=100))
        p_sum = 0
        for point in points:
            p_sum += int(point)
        print(newDicId+'的下一期psum:' + str(p_sum))

if __name__ == '__main__':
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='caipiaodata',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    # 创建表的操作
    cursor = connection.cursor()
    sql = 'select * from cptb'
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)

    newDic = getNewDataFromfucai()
    print('newDic == '+str(newDic))

    #开始计算推荐
    # calculBest(newDic,oldDatas=results)
