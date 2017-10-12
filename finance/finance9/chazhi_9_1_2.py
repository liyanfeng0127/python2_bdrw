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

x = np.linspace(-2 * np.pi , 2 * np.pi , 25)
def f(x):
    return np.sin(x) + 0.5 * x

ipo = spi.splrep(x ,f(x) , k=1)
iy = spi.splev(x, ipo)
plt.plot(x , f(x) , 'b' ,label= 'f(x)')
plt.plot(x , iy , 'r.' ,label= 'interpolation')
plt.legend(loc= 0)
plt.grid(True)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()


