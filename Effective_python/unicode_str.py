#-*-coding:utf8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#编写unicode和strshi ,输出Unicode
def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        value = unicode_or_str.decode('utf-8')
    else:
        value = unicode_or_str
    return value

#编写unicode和strshi ,输出str
def to_str(unicode_or_str):
    if isinstance(unicode_or_str, unicode):
        value = unicode_or_str.encode('utf-8')
    else:
        value = unicode_or_str
    return value



def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)
#结果[2, 3, 5, 7, 1, 4, 6, 8]


def sort_priority2(values, group):
    found = [False]
    def helper(x):
        if x in group:
            found[0] = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found[0]
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
found = sort_priority2(numbers, group)
print("Found:", found)
print(numbers)
#结果[2, 3, 5, 7, 1, 4, 6, 8]

def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset
with open('/xxx/address.txt') as f:
    it = index_file(f)
    results = islice(it, 0, 3)
    print(list(results))


