#-*-coding:utf8-*-

import requests
import json
import re

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'}


jscontent = requests.get('http://coral.qq.com/article/1165021596/comment?commentid=0&reqnum=50',headers=head).content
# aex = re.compile(r'\w+[(]{1}(.*)[)]{1}')
# jscontent = aex.findall(jscontent)
jsDict = json.loads(jscontent, 'gbk')
jsData = jsDict['data']
comments = jsData['commentid']
for each in comments:
    print each['content']
    print each['timeDifference']
    print each['userinfo']['nick']
    print each['userinfo']['region']
    # print each



# jsCommentid = jsData['commentid']
# userinfo = jsCommentid['userinfo']
# Userinfo = comments['userinfo']
# for eachinfo in Userinfo:
#     print eachinfo['nick']
#     print eachinfo['region']