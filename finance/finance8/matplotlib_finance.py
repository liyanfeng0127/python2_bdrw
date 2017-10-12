# -*- coding: utf-8 -*-
import matplotlib.finance as mpf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import sys
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
# 黑体	SimHei
# 微软雅黑	Microsoft YaHei
# 微软正黑体	Microsoft JhengHei
# 新宋体	NSimSun
# 新细明体	PMingLiU
# 细明体	MingLiU
# 标楷体	DFKai-SB
# 仿宋	FangSong
# 楷体	KaiTi
# 仿宋_GB2312	FangSong_GB2312
# 楷体_GB2312	KaiTi_GB2312
reload(sys)
sys.setdefaultencoding('utf-8')


start = (2016 , 12 , 3)
end = (2017 , 3 , 3)
#易华健康股票从2016.12.03到2017.03.03明天开盘价、最高价、最低价、收盘价和成交量

quotes = mpf.quotes_historical_yahoo_ochl('000150.sz' , start , end)
# quotes1 = list(quotes[:, 0])
# print("开盘价：" + quotes1)
#quotes1 = mpf.quotes_historical_yahoo_ochl('600028.ss' , start , end) 中国石化

fig , ax = plt.subplots(figsize = (16 , 8))
fig.subplots_adjust(bottom = 0.2)
mpf._candlestick(ax , quotes , width=0.6 , colorup='r' , colordown='b' )
#mpf._plot_day_summary(ax , quotes , width=0.6 , colorup='r' , colordown='b')

plt.grid(True)
ax.xaxis_date()
ax.autoscale_view()
plt.title(u'华谊健康K线图')
plt.ylabel('index level')
plt.setp(plt.gca().get_xticklabels(), rotation = 30)
plt.show()
