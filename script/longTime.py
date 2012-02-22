#-*- coding:utf-8 -*-
import time
import MySQLdb

begin = [2011, 1, 1, 0, 0, 0, 0, 0, 0]
begin = time.mktime(begin)


con = None
cursor = None

def exe(sql):
    print sql
    cursor.execute(sql)
    con.commit()
while True:
    now = time.mktime(time.localtime())
    now -= begin
    bon = int(now - 24*3600*30)

    con = MySQLdb.connect(host='localhost', user='root', passwd='badperson3', db = 'stcHong', charset = 'utf8')
    cursor = con.cursor()
    s = 'update operationalData set empirename = \'empty\', infantrypower = 0, cavalrypower = 0, defencepower = 0, logintime = '+str(bon) + ' where userid != 2800 and logintime < ' + str(bon)
    exe(s)
    s = 'update emptyCastal set uid = -1, inf = 0, cav = 0, lasttime = '+str(bon)+ ' where lasttime < '+str(bon)
    exe(s)
    time.sleep(3600*24)



