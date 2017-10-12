#-*-coding:utf8-*-

import sys
# from __future__ import division
import nltk , re , pprint
from urllib import urlopen
from bs4 import BeautifulSoup as BS
import feedparser

reload(sys)
sys.setdefaultencoding('utf-8')

# #解读文本格式
# url = 'http://www.gutenberg.org/files/2554/2554-0.txt'
# # proxies = {'http' : 'http://www.someproxy.com:3128'}
# raw = urlopen(url).read()
# # print raw[: 75]
# #raw现在是字符串，要将其改成list
# tokens = nltk.word_tokenize(raw)
# # print tokens[: 13]
# text = nltk.Text(tokens)
# print text[1020 : 1060]

# #解读HTML格式内容
# url2 = "http://www.gutenberg.org/files/2554/2554-h/2554-h.htm"
# html = urlopen(url2).read()
# # raw2 = nltk.clean_html(html)因为版本原因而无法使用
# #将HTML字符串作为参数，返回原始文本，进行分词，获得文本结构
# soup = BS(html)
# raw2 = BS.get_text(soup)
# tokens2 = nltk.word_tokenize(raw2)
# tokens2 = tokens2[96 : 399 ]
# text = nltk.Text(tokens2)
# print text.concordance('gene')

#处理RSS订阅
llog = feedparser.parse("http://languagelog.ldc.upenn.edu/nll/?feed=atom")
# print llog['feed']['title']
print llog
post = llog.entries[2]
content = post.content[0].value
# text1 = nltk.word_tokenize(BS.get_text(content))
# print text1