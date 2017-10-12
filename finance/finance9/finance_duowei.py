#-*-coding:utf8-*-

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm

reload(sys)
sys.setdefaultencoding('utf-8')

def fm((x, y)):
    return np.sin(x) + 0.25 * x + np.sqrt(y) + 0.05 * y ** 2

x = np.linspace(0 , 10 ,20)
y = np.linspace(0 , 10 ,20)
X , Y = np.meshgrid(x, y)
Z = fm((X ,Y))
x = X.flatten()
y = Y.flatten()
#建立三维坐标
fig = plt.figure(figsize=(9 , 6))
ax = fig.gca(projection= '3d')
surf = ax.plot_surface(X, Y ,Z ,rstride= 2, cstride=2, cmap= matplotlib.cm.coolwarm,
                       linewidth= 0.5 , antialiased=True)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
fig.colorbar(surf , shrink= 0.5 , aspect= 5)

matrix = np.zeros((len(x) , 7))
matrix[:,6] = np.sqrt(y)
matrix[:,5] = np.sin(x)
matrix[:,4] = y ** 2
matrix[:,3] = x ** 2
matrix[:,2] = y
matrix[:,1] = x
matrix[:,0] = 1
#statsmodels提供通用和有益的函数OLS，可以用于一维或者多维最小二乘回归
model =sm.OLS(fm((x, y)) , matrix).fit()
a = model.params

def reg_func(a , (x,y)):
    f6 = a[6] * np.sqrt(y)
    f5 = a[5] * np.sin(x)
    f4 = a[4] * y ** 2
    f3 = a[3] * x ** 2
    f2 = a[2] * y
    f1 = a[1] * x
    f0 = a[0] * 1
    return (f6 + f5 + f4 + f3 + f2 + f1 + f0)

RZ = reg_func(a , (X,Y))
fig = plt.figure(figsize=(9 , 6))
ax1 = fig.gca(projection= '3d')
surf1 = ax1.plot_surface(X, Y ,Z ,rstride= 2, cstride=2, cmap= matplotlib.cm.coolwarm,
                       linewidth= 0.5 , antialiased=True)
surf2 = ax1.plot_wireframe(X, Y ,Z ,rstride= 2, cstride=2, label= 'regression')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('f(x,y)')
ax1.legend()
fig.colorbar(surf , shrink= 0.5 , aspect= 5)
plt.show()
