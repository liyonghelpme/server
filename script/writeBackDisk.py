import MySQLdb
import time
con = MySQLdb.connect(host = 'localhost', db='stcHong', user='root', passwd='badperson3')
cursor = con.cursor()

while True:
    sql = 'select bid, city_id, ground_id, grid_id, object_id, producttime, finish  from businessWrite1 where `write` = 1'
    try:
        cursor.execute(sql)
    except:
        con = MySQLdb.connect(host = 'localhost', db='stcHong', user='root', passwd='badperson3')
        cursor = con.cursor()
        cursor.execute(sql)
    sql = 'update businessWrite1 set `write` = 0'
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        sql = 'update businessWrite set ground_id = '+str(d[2])+', grid_id = '+str(d[3])+', object_id = '+str(d[4])+', producttime = '+str(d[5])+', finish = '+str(d[6])+'  where bid = '+str(d[0])
        cursor.execute(sql)
    time.sleep(5*60)
