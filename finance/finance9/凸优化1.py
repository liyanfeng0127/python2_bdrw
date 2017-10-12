#-*-coding:utf8-*-

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm
import scipy.interpolate as spi

reload(sys)
sys.setdefaultencoding('utf-8')

def fm((x,y)):
    return (np.sin(x) + 0.5 * x ** 2 + np.sin(y) + 0.5 * y ** 2)

x = np.linspace(-10, 10, 50)
y = np.linspace(-10, 10 ,50)
X, Y = np.meshgrid(x,y)
Z = fm((X,Y))

fig = plt.figure(figsize=(9,6))
ax = fig.gca(projection= '3d')
surf = ax.plot_surface(X, Y ,Z ,rstride= 2, cstride=2, cmap= matplotlib.cm.coolwarm,
                       linewidth= 0.5 , antialiased=True)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
fig.colorbar(surf , shrink= 0.5 , aspect= 5)

plt.show()
