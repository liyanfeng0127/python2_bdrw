import numpy as np
from sklearn.metrics import confusion_matrix , classification_report
from sklearn.preprocessing import LabelBinarizer
from sklearn.cross_validation import train_test_split
from NN1 import NeuralNetwork
from sklearn.datasets import load_digits

digits = load_digits()
X = digits.data
y = digits.target
X -= X.min()
X /= X.max()

nn = NeuralNetwork([64 , 100 , 10] , 'logistic')
X_train , X_test , y_train , y_test = train_test_split(X , y)
labels_train = LabelBinarizer().fit_transform(y_train)
labels_test = LabelBinarizer().fit_transform(y_test)
print "start fitting"
nn.fit(X_train , labels_train ,epoch= 10000)
predictions = []
for i in range(X_test.shape[0]):
    o = nn.predict(X_test[i])
    predictions.append(np.argmax(o))
print confusion_matrix(y_test , predictions)
print classification_report(y_test , predictions)
