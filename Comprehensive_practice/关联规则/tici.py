#-*-coding:utf8-*-

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

output = u'分栏岗位.csv'
inputfile = u'G://PyCharm//data//预处理_岗位描述.csv'
path = u"G://PyCharm//data//合并.txt"

a = []
with open(path,'rb') as f:
    for line in f.readlines():
        a.append(line)
b=[]
c=[]
for i in range(len(a)):
    a[i]=a[i].strip()
import re,csv
# for model in a:
#     c.append(re.compile(model.strip()))
csv_reader = csv.reader(open(inputfile))
count=0
for line in csv_reader:
    b.append([])
    for model in a:
        try:
            if re.search(model,line[0].decode('gb2312').encode('utf-8')):
                b[-1].append(model)
        except UnicodeDecodeError:
            count+=1


csv_writer = csv.writer(open(output,'wt'))
for line in b:
    csv_writer.writerow(line)
