# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib

def urlopen():
    url = 'http://blog.kamidox.com/no-exist'
    try:
        s = urllib2.urlopen(url, timeout=3)
    except urllib2.HTTPError, e:
        print(e)
    else:
        print(s.read(100))
        s.close()


def request():
    # 定制 HTTP 头
    headers = {'User-Agent': 'Mozilla/5.0', 'x-my-header': 'my value'}
    req = urllib2.Request('http://blog.kamidox.com', headers=headers)
    s = urllib2.urlopen(req)
    print(s.read(100))
    print(req.headers)
    s.close()


def request_post_debug():
    # POST
    data = {'username': 'kamidox', 'password': 'xxxxxxxx'}
    # headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'plain/text'}
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request('http://www.douban.com', data=urllib.urlencode(data), headers=headers)
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
    s = opener.open(req)
    print(s.read(100))
    s.close()


def install_debug_handler():
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1),
                                  urllib2.HTTPSHandler(debuglevel=1))
    urllib2.install_opener(opener)


def handle_cookie():
    cookiejar = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookiejar=cookiejar)
    opener = urllib2.build_opener(handler, urllib2.HTTPHandler(debuglevel=1))
    s = opener.open('http://www.douban.com')
    print(s.read(100))
    s.close()

    print('=' * 80)
    print(cookiejar._cookies)
    print('=' * 80)

    s = opener.open('http://www.douban.com')
    s.close()


if __name__ == '__main__':
    handle_cookie()