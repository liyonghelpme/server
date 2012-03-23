import MySQLdb
import time

con = MySQLdb.connect(host = 'localhost', db='stcHong', user='root', passwd='badperson3')
cursor = con.cursor()

def exe(sql):
    print sql
    cursor.execute(sql)
while True:
    sql = 'select bid, city_id, ground_id, grid_id, object_id, producttime, finish  from businessWrite1 where `write` = 1'
    try:
        exe(sql)
        #cursor.execute(sql)
    except:
        con = MySQLdb.connect(host = 'localhost', db='stcHong', user='root', passwd='badperson3')
        cursor = con.cursor()
        cursor.execute(sql)

    data = cursor.fetchall()
    data = list(data)

    for d in data:
        sql = 'update businessWrite set ground_id = '+str(d[2])+', grid_id = '+str(d[3])+', object_id = '+str(d[4])+', producttime = '+str(d[5])+', finish = '+str(d[6])+'  where bid = '+str(d[0])
        #cursor.execute(sql)
        exe(sql)

    sql = 'update businessWrite1 set `write` = 0'
    exe(sql)


    #cursor.execute(sql)

    time.sleep(5*60)
