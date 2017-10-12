#-*-coding:utf8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def mergesort(seq):
    mid = len(seq) // 2
    lft, rgt = seq[:mid], seq[mid:]
    if len(lft) > 1:
        lft = mergesort(lft)
    if len(rgt) > 1:
        rgt = mergesort(rgt)
    res = []
    while lft and rgt:
        if lft[-1] >= rgt[-1]:
            res.append(lft.pop())
        else:
            res.append(rgt.pop())

    res.reverse()
    return (lft + rgt) + res


a = [3, 5, 10, 34, 24, 2, 25, 15, 8]
print mergesort(a)