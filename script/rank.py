#!/usr/bin/env python   
#coding=utf-8

import MySQLdb
import time

conn = MySQLdb.connect(host='localhost',user='root',passwd='badperson3',db='stcHong')
cursor = conn.cursor()
logfile = open("/root/tg2env/stchong/ranklog","a")
#print "####### wonder_empire daily rank at "+time.strftime("%Y-%m-%d %H:%M:%S ",time.localtime())+" #######"
logfile.write("####### wonder_empire daily rank at "+time.strftime("%Y-%m-%d %H:%M:%S ",time.localtime())+" #######\n")
#0userid,1corn,2otherid,3lev,4food
#sql = "select userid,corn,otherid,lev,food,exp from operationalData where userid >3260 and userid!=3613 and userid!=3829 and userid!=5500 and userid!=10770 and userid!=13336 and userid!=3397"
sql = "select userid,corn,otherid,lev,food,exp from operationalData where userid >3260 and userid!=3613 and userid!=3829 and userid!=5500 and userid!=10770 and userid!=13336 limit 999"
cursor.execute(sql)
results = cursor.fetchall()
temp = []
user = []
ranks = []
food_ranks = []
exp_ranks = []
ranks_item = []

for r in results:
    user = list(r)
    temp.append(user)
temp.sort(key=lambda x:(x[1],x[3]))
temp.reverse()


#fortune rank
i = 1
rank = 1
fortune2 = 0
for r in temp:
    userid = r[0]
    corn = r[1]
    otherid = r[2]
    lev = r[3]
    food = r[4]
    exp = r[5]
    ranks_item.append(userid)
    ranks_item.append(otherid)
    if i != 1:
        fortune2 = corn
        if(fortune2 == fortune1 and lev == lev1):
            ranks_item.append(rank)
        else:
            rank = i
            ranks_item.append(rank)
        fortune1 = fortune2
        lev1 = lev
    else:
        fortune1=corn
        lev1 = lev
        ranks_item.append(rank)
    ranks_item.append(corn)
    ranks_item.append(lev)
    ranks_item.append(food)
    ranks_item.append(exp)
    ranks.append(ranks_item)
    ranks_item = []
    i = i + 1
#print ranks
#logfile.write(str(ranks)+"\n")

#foodrank 0userid,1otherid,2fortunerank,3corn,4lev,5food,6exp
ranks.sort(key=lambda x:(x[5],x[4]))
ranks.reverse()
i = 1
rank = 1
food2 = 0
ranks_item = []
for r in ranks:
    userid = r[0]
    otherid = r[1]
    fortunerank = r[2]
    corn = r[3]
    lev = r[4]
    food = r[5]
    exp = r[6]
    ranks_item.append(userid)
    ranks_item.append(otherid)
    ranks_item.append(fortunerank)
    ranks_item.append(corn)
    if i != 1:
        food2 = food
        if(food2 == food1 and lev == lev1):
            ranks_item.append(rank)
        else:
            rank = i
            ranks_item.append(rank)
        food1 = food2
        lev1 = lev
    else:
        food1=food
        lev1 = lev
        ranks_item.append(rank)
    ranks_item.append(food)
    ranks_item.append(exp)
    ranks_item.append(lev)
    food_ranks.append(ranks_item)
    ranks_item = []
    i = i + 1

#exprank 0userid,1otherid,2fortunerank,3corn,4foodrank,5food,6exp,7lev
food_ranks.sort(key=lambda x:(x[6]))
food_ranks.reverse()
i = 1
rank = 1
exp2 = 0
ranks_item = []
for r in food_ranks:
    userid = r[0]
    otherid = r[1]
    fortunerank = r[2]
    corn = r[3]
    foodrank = r[4]
    food = r[5]
    exp = r[6]
    lev = r[7]
    ranks_item.append(userid)
    ranks_item.append(otherid)
    ranks_item.append(fortunerank)
    ranks_item.append(corn)
    ranks_item.append(foodrank)
    ranks_item.append(food)
    if i != 1:
        exp2 = exp
        if(exp2 == exp1):
            ranks_item.append(rank)
        else:
            rank = i
            ranks_item.append(rank)
        exp1 = exp2
    else:
        exp1 = exp
        ranks_item.append(rank)
    ranks_item.append(exp)
    ranks_item.append(lev)
    exp_ranks.append(ranks_item)
    ranks_item = []
    i = i + 1

#insert into ranks
#0userid,1otherid,2fortunerank,3corn,4foodrank,5food,6exprank,7exp,8lev
cursor.execute("delete from rank where userid > 3260")
num=0
for r in exp_ranks:
    num = num + 1
#    print r
    sql="insert into rank (userid,otherid,meritrank,power,fortunerank,corn,foodrank,food,exprank,exp,lev) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    param = (r[0],r[1],0,0,r[2],r[3],r[4],r[5],r[6],r[7],r[8])
    cursor.execute(sql,param)

#merit rank
#0uid,1won,2power(except out power in battle)
#sql = "select victories.uid,victories.won,operationalData.infantrypower+operationalData.cavalrypower+operationalData.defencepower,operationalData.nobility*3+operationalData.subno from victories,operationalData where uid > 3260 and userid!=3613 and userid!=5500 and userid!=3829 and userid!=10770 and userid!=13336 and userid!=3397  and victories.uid=operationalData.userid"
sql = "select victories.uid,victories.won,operationalData.infantrypower+operationalData.cavalrypower+operationalData.defencepower,operationalData.nobility*3+operationalData.subno from victories,operationalData where uid > 3260 and userid!=3613 and userid!=5500 and userid!=3829 and userid!=10770 and userid!=13336 and victories.uid=operationalData.userid"
cursor.execute(sql)
results = cursor.fetchall()
temp = []
users = []
for res in results:
    r = list(res)
    uid = r[0]
    won = r[1]
    power = r[2]
    nobilitynum = r[3]
    sql_battle = "select sum(power) from battle group by uid having uid=%s"
    param = (r[0])
    cursor.execute(sql_battle,param)
    outpower=cursor.fetchall()
#    print outpower
    if len(outpower)==0 or outpower==None:
        power = power
    else:
        power = power + int(outpower[0][0])
    temp.append(r[0])
    temp.append(won)
    temp.append(power)
    temp.append(nobilitynum)
    users.append(temp)
    temp = []
#users:0uid,1won,2power,3nobilitynum

#print users
users.sort(key=lambda x:(x[3],x[1],x[2]))
users.reverse()
#print users

i = 1
rank = 1
win1 = 0
lose1 = 0
power1 = 0
for u in users:
    if i!=1:
        if(u[1]==win1 and u[2]==power1):
            u.append(rank)
        else:
            rank = i
            u.append(rank)
        win1 = u[1]
        power1 = u[2]
    else:
        win1 = u[1]
        power1 = u[2]
        u.append(rank)
    i = i+1
#print users
#logfile.write(str(users)+"\n\n")

#insert into rank:merit
#users:0uid,1won,2power,3nobilitynum,4rank
for u in users:
    sql="update rank set meritrank=%s,nobilitynum=%s,won=%s,power=%s where userid=%s"
    param=(u[4],u[3],u[1],u[2],u[0])
    cursor.execute(sql,param)

logfile.close()
cursor.close() 
conn.close()
