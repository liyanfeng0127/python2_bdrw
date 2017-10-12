#-*-coding:utf8-*-

import sys
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')

proc = subprocess.Popen(['echo', 'hello world the child!'], stdout= subprocess.PIPE)
out, err = proc.communicate()
print(out.decode('utf-8'))