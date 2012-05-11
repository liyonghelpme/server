import json
f = json.loads(open('1000').read())
import MySQLdb
con = MySQLdb.connect(host='localhost', user='root', password='wavegame1', db='stcHong')
cur = con.cursor()

for i in f[:800]:
    oid = i[0]
    sql = 'select userid from operationalData where otherid = \''+str(oid)+'\''
    cur.execute(sql)
    d = cur.fetchall()
    print d[0][0]

