# -*- coding: utf-8 -*-

import matplotlib.finance as mpf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pylab import *
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体为黑体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

start = (2016 , 12, 3)
end = (2017 , 3 , 3)
quotes = np.array(mpf.quotes_historical_yahoo_ochl('000150.sz' , start , end))

fig,(ax1,ax2)= plt.subplots(2, sharex=True, figsize=(20, 30))
mpf._candlestick(ax1 , quotes, width= 0.6 , colorup= 'r' , colordown='b')
ax1.set_title(u'易华健康 Inc.')
ax1.set_ylabel('index level')
ax1.grid(True)
ax1.xaxis_date()
plt.bar(quotes[: , 0] - 0.25 , quotes[: , 5] , width= 0.5 , color = 'y')
ax2.set_ylabel('volume')
ax2.grid(True)
ax2.autoscale_view()
plt.setp(plt.gca().get_xticklabels() , rotation = 30)
plt.show()