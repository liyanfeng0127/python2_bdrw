#-*-coding:utf8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Registry(object):
    def __init__(self):
        self._function = []

    def register(self, decorated):
        self._function.append(decorated)
        return decorated

    def run_all(self, *arg, **kwargs):
        return_values = []
        for func in self._function:
            return_values.append(func(*arg, **kwargs))
        return return_values



a = Registry()
b = Registry()

@a.register
def foo(x= 3):
    return x

@b.register
def bar(x= 5):
    return x

@a.register
@b.register
def baz(x=7):
    return x

print a.run_all()
print b.run_all()




