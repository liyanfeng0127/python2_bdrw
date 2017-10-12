#-*-coding:utf8-*-

import smtplib
from email.mime.text import MIMEText
import requests
from lxml import etree
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class mailhelper(object):
    '''
    这个类实现发送邮件的功能
    '''
    def __init__(self):

        self.mail_host="smtp.qq.com"  #设置服务器
        self.mail_user=u"那也不行"    #用户名
        self.mail_pass="2319619ld"   #密码
        self.mail_postfix="qq.com"  #发件箱的后缀

    def send_mail(self,to_list,sub,content):
        me="xxoohelper"+"<"+self.mail_user+"@"+self.mail_postfix+">"
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user,self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False


class xxoohelper(object):
    '''
    这个类实现将爬取微博第一条内容
    '''
    def __init__(self):
        self.url = 'https://bbs.pku.edu.cn/v2/thread.php?bid=896' #请输入准备抓取的微博地址
        # self.url_login = 'https://login.weibo.cn/login/'
        # self.new_url = self.url_login

    def getSource(self):
        html = requests.get(self.url).content
        return html

    def getData(self,html):
        selector = etree.HTML(html)
        #//*[@id="list-content"]
        password = selector.xpath('//input[@type="password"]/@name')[0]
        vk = selector.xpath('//input[@name="vk"]/@value')[0]
        action = selector.xpath('//form[@method="post"]/@action')[0]
        self.new_url = self.url_login + action
        data = {
            'mobile' : 'xxxxx@xxx.com',
             password : 'xxxxxx',
            'remember' : 'on',
            'backURL' : 'http://weibo.cn/u/xxxxxx', #此处请修改为微博地址
            'backTitle' : u'微博',
            'tryCount' : '',
            'vk' : vk,
            'submit' : u'登录'
            }
        return data

    def getContent(self,data):
        newhtml = requests.post(self.new_url,data=data).content
        new_selector = etree.HTML(newhtml)
        content = new_selector.xpath('//span[@class="ctt"]')
        newcontent = unicode(content[2].xpath('string(.)')).replace('http://','')
        sendtime = new_selector.xpath('//span[@class="ct"]/text()')[0]
        sendtext = newcontent + sendtime
        return sendtext

    def tosave(self,text):
        f= open('weibo.txt','a')
        f.write(text + '\n')
        f.close()

    def tocheck(self,data):
        if not os.path.exists('weibo.txt'):
            return True
        else:
            f = open('weibo.txt', 'r')
            existweibo = f.readlines()
            if data + '\n' in existweibo:
                return False
            else:
                return True



if __name__ == '__main__':
    mailto_list=['454552269@qq.com'] #此处填写接收邮件的邮箱
    helper = xxoohelper()
    while True:
        source = helper.getSource()
        data = helper.getData(source)
        content = helper.getContent(data)
        if helper.tocheck(content):
            if mailhelper().send_mail(mailto_list,u"招聘信息更新了！",content):
                print u"发送成功"
            else:
                print u"发送失败"
            helper.tosave(content)
            print content
        else:
            print u'pass'
        time.sleep(30)