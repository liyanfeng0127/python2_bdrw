
from ftplib import FTP
import os
ftp=FTP()
ftp.set_debuglevel(2)
ftp.connect('127.0.0.1','21')
ftp.login('liyanfeng','123')
list=ftp.nlst()
print ftp.nlst()#liebiao
for filename in list:
    if os.path.exists(filename):
        print 'File exists!'
    else:
        ftp.retrbinary("RETR %s" % filename, open(filename, 'wb').write, 1024)
        print filename + '   has been downloaded'

