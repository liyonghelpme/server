import json
f = open('incMon').readlines()
import MySQLdb
con = MySQLdb.connect(host='localhost', user='root', passwd='wavegame1', db='stcHong')
cur = con.cursor()

for i in f:
    oid = int(i.replace('\n', ''))
    sql = 'select userid from operationalData where otherid = \''+str(oid)+'\''
    cur.execute(sql)
    d = cur.fetchall()
    print d[0][0]

