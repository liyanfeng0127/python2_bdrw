import tushare as ts
from sqlalchemy import create_engine

engine = create_engine("mysql://root:1234@localhost/scraping?charset=utf8")

print ts.get_stock_basics()
df1 = ts.get_stock_basics()
df1.to_sql('news_data',engine,if_exists='append')
print df1
print ts.get_tick_data('600019',date = '2016-12-16')
df2 = ts.get_tick_data('600019',date = '2016-12-16')
print df2
print ts.get_latest_news()
df3 = ts.get_latest_news()
df3.to_sql('news_data',engine,if_exists='append')
print df3
