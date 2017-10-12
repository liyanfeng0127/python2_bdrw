import pymysql
conn = pymysql.connect(host ='localhost',port=3306,user = 'root',
                       passwd = '1234',db = 'scraping')

cur = conn.cursor()

cur.execute("use scraping")
cur.execute("select * from pages where id=1")
print cur.fetchone()
cur.close()
conn.close()