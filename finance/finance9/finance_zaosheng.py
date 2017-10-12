#-*-coding:utf8-*-

import sys
import numpy as np
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf-8')

def f(x):
    return np.sin(x) + 0.5 * x
#linspace(start , end , num)返回从start开始，stop结束的num个点，两个连续点之间的均匀分布
xn = np.linspace(-2 * np.pi, 2 * np.pi , 50)
xn = xn + 0.25 * np.random.standard_normal(len(xn))
yn = f(xn) + 0.25 * np.random.standard_normal(len(xn))


#回归
#x坐标（自变量）、y（因变量）、deg多项式拟合、full：真，则返回额外的诊断信息、
# w应用到y坐标权重、cov：真，则返回协方差矩阵
reg = np.polyfit(xn , yn , deg= 11)
ry = np.polyval(reg , xn)

plt.plot(xn , yn , 'b^' ,label= 'f(x)')
plt.plot(xn , ry , 'ro' ,label= 'regression')
plt.legend(loc= 0)
plt.grid(True)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()


