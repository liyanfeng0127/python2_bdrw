#-*-coding:utf8-*-

import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

HYJK = web.DataReader(name= '000150.sz' , data_source= 'yahoo' , start= '2016-1-1')
HYJK.info()
HYJK.tail()
# plt.show(HYJK['Close'].plot(figsize=(8 , 5)))

HYJK['Ret_Loop'] = 0.0
for i in range(1 , len(HYJK)):
    HYJK['Ret_Loop'][i] = np.log(HYJK['Close'][i] / HYJK['Close'][i - 1])
print HYJK[['Close' , 'Ret_Loop']].tail()

HYJK['Return'] = np.log(HYJK['Close'] / HYJK['Close'].shift(1))

# print HYJK[['Close' , 'Ret_Loop' , 'Return']].tail()
# HYJK[['Close' , 'Return']].plot(subplots=True , style='b' , figsize=(8 , 5))
# plt.show()
#移动平均值使用pandas的rolling_mean函数计算,但是rolling_mean()函数被替换成rolling().mean()
HYJK['30d'] = pd.rolling_mean(HYJK['Close'] , window=30)
HYJK['150d'] = pd.rolling_mean(HYJK['Close'] , window=150)
HYJK[['Close' , '30d' , '150d']].plot(figsize=(8,5))
# plt.show()

HYJK['Mov_Vol'] = pd.rolling_std(HYJK['Return'] , window=150) * math.sqrt(150)
HYJK[['Close' , 'Mov_Vol' , 'Return']].plot(subplots=True , style='b' , figsize=(8,7))

