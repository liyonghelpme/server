import os,sys,string
import MySQLdb


try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='2e4n5k2w2x',db='stcHong')
except Exception, e:
    print e
    sys.exit()
cursor=conn.cursor()
sql="delete from gift"
try:
    cursor.execute(sql)
except Excepttion,e:
    print e
    sys.exit()
    
sql="delete from news"
try:
    cursor.execute(sql)
except Exception, e:
    print e
    sys.exit()
    
conn.commit()
