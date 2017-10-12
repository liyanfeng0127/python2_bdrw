# coding:utf-8

import urllib

def print_list(list):
    for i in list:
        print(i)

def demo():
    s = urllib.urlopen('http://blog.kamidox.com')
    msg = s.info()
    s.getcode()
    print_list(msg.status)
    # for i in range(10):
    #     print ('line is %d : %s ' % (i + 1, s.readline()))
    #print(s.read(100))

def retrieve():
    fname , msg = urllib.urlretrieve('http://blog.kamidox.com')
    print(fname)
    print_list(msg.items())

if __name__ == '__main__':
    #demo()
    retrieve()