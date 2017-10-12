#-*-coding:utf8-*-

import sys
from pprint import pprint


reload(sys)
sys.setdefaultencoding('utf-8')


class SimpleGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count

class MyBaseClass(object):
    def __init__(self, value):
        self.value = value

class TimeFiveCorret(MyBaseClass):
    def __init__(self,value):
        super(TimeFiveCorret, self).__init__(value)
        self.value *= 5

class PlusTwoCorret(MyBaseClass):
    def __init__(self, value):
        super(PlusTwoCorret, self).__init__(value)
        self.value += 2

class GoodWay(TimeFiveCorret, PlusTwoCorret):
    def __init__(self, value):
        super(GoodWay, self).__init__(value)

foo = GoodWay(5)
print foo.value
pprint(GoodWay.mro())
# 35
# [<class '__main__.GoodWay'>,
#  <class '__main__.TimeFiveCorret'>,
#  <class '__main__.PlusTwoCorret'>,
#  <class '__main__.MyBaseClass'>,
#  <type 'object'>]

#用min-in把二叉树表示为字典
