# -*- coding: utf-8 -*-

from lxml import etree
import requests
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

def spider(url):
    html = requests.get(url).content
    #f.writelines(html)
    selector = etree.HTML(html.decode('utf-8'))
    table = selector.xpath('//body/div[@class="bg"]')
    for each in table:
        #/html/body/div[9]/div/center/table/tbody/tr[1]/td/center/h2
        Content = each.xpath('div[@class="mulu"]/center/table/tbody/tr/td[@colspan="3"]/center/h2/text()')
        #print Content
        # for eachcontent in Content:
        #     bookName = eachcontent.xpath('td[@colspan="3"]/center/h2/text()')
        #     print bookName
        content = each.xpath('div[@class="mulu"]/center/table/tbody/tr')
        print content
        # url = each.xpath('tr/td/a/@href')
        # for i in range(len(url)):
        #     # 为了防止后一个数据覆盖前一个数据，需要在每个循环里都实例化一个NovelspiderItem
        #     item['bookName'] = bookName
        #     item['chapterURL'] = url[i]
        #     # try可以用于检测错误，出现错误以后就会运行except里面的内容。
        #     try:
        #         item['bookTitle'] = content[i].split(' ')[0]
        #         item['chapterNum'] = content[i].split(' ')[1]
        #     except Exception, e:
        #         continue
        #
        #     try:
        #         item['chapterName'] = content[i].split(' ')[2]
        #     except Exception, e:
        #         item['chapterName'] = content[i].split(' ')[1][-3:]
        #     #print item


if __name__ == '__main__':
    #f = open('forum.txt','a')
    newpage = 'http://www.daomubiji.com/'
    spider(newpage)
    #f.close()