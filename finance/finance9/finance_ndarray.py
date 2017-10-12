#-*-coding:utf8-*-

import sys
import numpy as np
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf-8')

def f(x):
    return np.sin(x) + 0.5 * x

#linspace(start , end , num)返回从start开始，stop结束的num个点，两个连续点之间的均匀分布
x = np.linspace(-2 * np.pi, 2 * np.pi , 50)

matrix = np.zeros((4 ,len(x)))
matrix[3,:] = np.sin(x)
matrix[2,:] = x ** 2
matrix[1,:] = x
matrix[0,:] = 1

reg = np.linalg.lstsq(matrix.T , f(x))[0]

ry = np.dot(reg , matrix)
plt.plot(x , f(x) , 'b' ,label= 'f(x)')
plt.plot(x , ry , 'r.' ,label= 'regression')
plt.legend(loc= 0)
plt.grid(True)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()

