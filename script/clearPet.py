import MySQLdb
import json

con = MySQLdb.connect(host='localhost', user='root', db='stcHong', passwd='2e4n5k2w2x')
cursor = con.cursor()

sql = "select pid, friList, lastFeed, state, health  from dragon where state >= 2"
cursor.execute(sql)
print sql
allData = cursor.fetchall()
for data in allData:
    print str(data)
    pid = data[0]
    friList = data[1]
    lastFeed = data[2]
    state = data[3]
    health = data[4]
    #not update attack
    if state > 1: #0 not active 1 buy egg 2 egg
        if lastFeed == 0:#not feed
            if state == 2:#egg
                health -= 1
            elif state == 3:#child
                health -= 1
            elif state == 4:#young
                health -= 2
            elif state == 5:#old
                health -= 10
        else:
            #if state == 5:
            #    health -= 10
            friList = '[]'
            lastFeed = 0
        if health < 0 :#no dead at all
            #if state == 5:
            #    state = -1 #dead
           # else:
            health = 0
        sql = "update dragon set health = " + str(health) + ', lastFeed = ' + str(lastFeed)+', friList = \''+str(friList) + '\',trainNum=0 where pid = ' + str(pid)
        print sql
        cursor.execute(sql)
        con.commit()


            
