import os,sys,string
import MySQLdb
import random
import time

while True:
    try:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='badperson3',db='stcHong')
    except Exception, e:
        print e

    cursor = conn.cursor()

    sql = 'select mid from monster group by mid'
    cursor.execute(sql)
    monsters = cursor.fetchall()

    nmon = []
    for m in monsters:
        nmon.append(m[0])
    nmon = set(nmon)
    print nmon
        
    sql = 'select mapid, map_kind from warMap where mapid != -1 group by mapid'
    cursor.execute(sql)
    maps = cursor.fetchall()
    print maps

    draNum = [10, 20, 40, 80]
    def getMonster(mid, kind):
        base = draNum[min(kind, len(draNum)-1)] 
        dragonNum = random.randint(base, base+5)
        power = dragonNum*300

        sql = 'insert into monster (mid, power, attacker, dragonNum) values(%d, %d, %s, %d)' % (mid, power, '\'[]\'', dragonNum) 
        print sql
        cursor.execute(sql)
        
    for m in maps:#m[0] = mapid
        if m[0] not in nmon:
            getMonster(m[0], m[1])
    conn.commit()

    time.sleep(3600*12)


            
        


