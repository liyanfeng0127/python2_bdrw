#-*-coding:utf8-*-
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

'''重新运行之前请删除content.txt，因为文件操作使用追加方式，会导致内容太多。'''

def towrite(contentdict):
    # f.writelines(u'回帖时间:' + str(contentdict['topic_reply_time']) + '\n')
    # f.writelines(u'回帖内容:' + unicode(contentdict['topic_reply_content']) + '\n')
    # f.writelines(u'回帖人:' + contentdict['user_name'] + '\n\n')
    pass

def spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    # print selector
    #content_field = selector.xpath('//div[@class="l_post l_post_bright "]')
    content_field = selector.xpath('//div[@id="j_p_postlist"]/div')
    item = {}
    for each in content_field:
        # reply_info = json.loads(each.xpath('div/@data-field'))
        # #[0].replace('&quot',''))
        # print reply_info
        # author = reply_info['author']['user_name']
        #content = each.xpath('div[starts-with(@class,"l_post l_post_bright  ")]/div[@class="d_post_content_main"]/div[starts-with(@class,"p_content")]/cc/div[starts-with(@id,"post_content")]/text()')
        # content = each.xpath('div[starts-with(@class,"l_post l_post_bright  ")]/div[@class="d_post_content_main"]/div[starts-with(@class,"p_content")]/cc')[0]
        content = each.xpath('div[@class="d_post_content_main"]/div[@class="p_content  p_content p_content_nameplate"]/cc')
        print content
        content = list(content.xpath('string(.)'))
        content = ''.join(content)
        # reply_time = reply_info['content']['date']
        # item['user_name'] = author
        item['topic_reply_content'] = content
        # item['topic_reply_time'] = reply_time
        print item
        towrite(item)

if __name__ == '__main__':
    # pool = ThreadPool(4)
    f = open('content.txt','a')
    page = []
    for i in range(1,21):
        newpage = 'http://tieba.baidu.com/p/3522395718?pn=' + str(i)
        page.append(newpage)
    results = map(spider, page)
    # pool.close()
    # pool.join()
    f.close()


