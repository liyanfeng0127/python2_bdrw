from sklearn.feature_extraction import DictVectorizer
import csv
from sklearn import preprocessing
from sklearn import tree
from sklearn.externals.six import StringIO

allElectronicsData = open(r'G:\PyCharm\ceshi.csv' , 'rb')
reader = csv.reader(allElectronicsData)
headers = reader.next()

print(headers)

featurelist = []
labelList = []

for row in reader:
    labelList.append(row[len(row) - 1])
    rowDict = {}
    for i in range(1 , len(row) - 1):
        rowDict[headers[i]] = row[i]
    featurelist.append(rowDict)

print(featurelist)
print labelList

vec = DictVectorizer()
dummyX = vec.fit_transform(featurelist) .toarray()

print("dummyX:" + str(dummyX))
print vec.get_feature_names()

print "labelList:" + str(labelList)

lb = preprocessing.LabelBinarizer()
dummyY = lb.fit_transform(labelList)
print "dummyY:" + str(dummyY)

clf = tree.DecisionTreeClassifier(criterion= 'entropy')
clf = clf.fit(dummyX , dummyY)
print "clf:" + str(clf)

with open("allElectronicInformationGainOri.dot" , 'w') as f:
    f = tree.export_graphviz(clf , feature_names= vec.get_feature_names() , out_file= f)

oneRowX = dummyX[0 , :]
print "oneRowX:" + str(oneRowX)

newRowX = oneRowX
newRowX[0] = 1
newRowX[2] = 0
print "newRowX:" + str(newRowX)

predictedY = clf.predict(newRowX)
print "predictedY:" + str(predictedY)