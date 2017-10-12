#-*-coding:utf8-*-
import pymongo

connection = pymongo.MongoClient()
tdb = connection.Jikexueyuan
post_info = tdb.test

jike = {'name':u'极客', 'age':'5', 'skill': 'Python'}
god = {'name': u'玉皇大帝', 'age': 36000, 'skill': 'creatanything', 'other': u'王母娘娘不是他的老婆'}
godslaver = {'name': u'月老', 'age': 'unknown', 'other': u'他的老婆叫孟婆'}
post_info.insert(jike)
post_info.insert(god)
post_info.insert(godslaver)
# post_info.remove({'name': u'极客'})

print u'操作数据库完成！'