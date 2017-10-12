import pandas as pd
from urllib import urlretrieve
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

es_url = 'https://www.stoxx.com/document/Indices/Current/HistoricalData/hbrbcpe.txt'
vs_url = 'https://www.stoxx.com/document/Indices/Current/HistoricalData/h_vstoxx.txt'
urlretrieve(es_url , './data/es.txt')
urlretrieve(vs_url , './data/vs.txt')

lines = open('./data/es.txt' , 'r').readlines()
lines = [line.replace(' ' , '') for line in lines]

new_file = open('./data/es50.txt' , 'w')
new_file.writelines('date' + lines[3][:-1] + ';Del' + lines[3][-1])
new_file.writelines(lines[4:])
new_file.close()

new_files = open('./data/es50.txt' , 'r').readlines()

es = pd.read_csv('./data/es50.txt' , index_col=0 , parse_dates=True ,
                 sep=';' , dayfirst=True)
print np.round(es.tail())
es.info()

cols = ['SX5P' , 'SX5E' , 'SXXP' , 'SXXE' , 'SXXF' , 'SXXA' , 'DK5F', 'DKXF']
es = pd.read_csv(es_url , index_col=0 , parse_dates=True , sep=';' ,
                 dayfirst=True , header=None , skiprows=4 , names=cols)
print es.tail()

vs = pd.read_csv('./data/vs.txt' , index_col=0 , header=2 , parse_dates=True ,
                 sep=';' , dayfirst=True)
vs.info()

data = pd.DataFrame({'EUROSTOXX' :
                    es['SX5E'][es.index > dt.datetime(1999 , 1 , 1)]})
data = data.join(pd.DataFrame({'VSTOXX' :
                    vs['V2TX'][vs.index > dt.datetime(1999 , 1 , 1)]}))
data = data.fillna(method='ffile')
data.info()
print data.tail()
data.plot(subplots=True , grid=True , style='b' , figsize=(8,6))
plt.show()

rets = np.log(data / data.shift(1))
rets.head()
rets.plot(subplots=True , grid=True , style='b' , figsize=(8,6))
plt.show()

xdat = rets['EUROSTOXX']
ydat = rets['VSTOXX']
model = pd.ols(y=ydat , x=xdat)
print model.beta

plt.plot(xdat , ydat , 'r.')
ax = plt.axis()
x = np.linspace(ax[0] , ax[1] + 0.01)
plt.plot(x , model.beta[1] + model.beta[0] * x , 'b' ,lw=2)
plt.grid(True)
plt.axis('tight')
plt.xlabel('EURO STOXX 50 returns')
plt.ylabel('VSTOXX returns')
rets.corr()
pd.rolling_corr(rets['EUROSTOXX'] , rets['VSTOXX'] , window=252).plot(grid=True , style='b')
