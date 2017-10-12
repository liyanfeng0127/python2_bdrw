# -*- coding: utf-8 -*-
import urllib
import datetime

def download_stock_data(stock_list):
    for sid in stock_list:
        url = 'http://table.finance.yahoo.com/table.csv?s=' + sid
        fname = sid + '.csv'
        print('downloading %s form %s' % (fname, url))
        urllib.urlretrieve(url, fname)


def download_stock_data_in_period(stock_list, start, end):
    for sid in stock_list:
        params = {'a': start.month - 1, 'b': start.day, 'c': start.year,
                  'd': end.month - 1, 'e': end.day, 'f': end.year, 's': sid}
        url = 'http://table.finance.yahoo.com/table.csv?'
        qs = urllib.urlencode(params)
        print qs
        url = url + qs
        print url
        fname = '%s_%d%d%d_%d%d%d.csv' % (sid, start.year, start.month, start.day,
                                          end.year, end.month, end.day)
        #print('downloading %s from %s' % (fname, url))
        urllib.urlretrieve(url, fname)
        urllib.urlopen(url)


if __name__ == '__main__':
    stock_list = ['300001.sz', '310002.sz']
    end = datetime.date(year=2015, month=12, day=17)
    start = datetime.date(year=2015, month=11, day=17)
    download_stock_data_in_period(stock_list, start, end)

