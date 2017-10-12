#-*-coding:utf8-*-

import sys
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')


def get_md5(url):
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == '__main__':
    #hashlib函数不接收Unicode编码，必须转换成utf-8模式
    print(get_md5("http://haogaozhong.eol.cn/school_area.php?"))