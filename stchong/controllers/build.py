# -*- coding: utf-8 -*-
"""Fallback controller."""

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import or_, and_, desc, select
from sqlalchemy import func


from stchong.model import DBSession, db 
import random
from stchong import model
import json
from stchong.controllers.util import *
from stchong.model import *
import time
import inspect

friendGod = [[2*3600, 500, 10000, 50, 100, 0], [6*3600, 1000, 20000, 100, 10, 5], [12*3600, 2000, 50000, 170, 10, 10], [18*3600, 5000, 100000, 250, 10, 15], [24*3600, 10000, 500000, 350, 10, 30]]
#coin food wood caesars exp buildTime specials size 
housebuild=[[500,10,0,0,3,600,None,1],[1400,30,0,1,8,1200,'a,1',1],[2800,0,70,2,15,2400,'a,2;b,3',1],[int(500*1.1),10,0,0,3,600,None,1],[int(1400*1.1),30,0,1,8,1200,'a,1',1],[int(2800*1.1),0,70,2,15,2400,'a,2;b,3',1],[int(500*1.2),10,0,0,3,600,None,1],[int(1400*1.2),30,0,1,8,1200,'a,1',1],[int(2800*1.2),0,70,2,15,2400,'a,2;b,3',1],[int(500*1.3),10,0,0,3,600,None,1],[int(1400*1.3),30,0,1,8,1200,'a,1',1],[int(2800*1.3),0,70,2,15,2400,'a,2;b,3',1],[1500,60,0,0,5,1800,None,5],[4800,120,0,3,13,4800,'b,2;c,2',5],[9000,0,100,4,24,9000,'c,2;d,3',5],[int(1500*1.1),60,0,0,5,1800,None,5],[int(4800*1.1),120,0,3,13,4800,'b,2;c,2',5],[int(9000*1.1),0,100,4,24,9000,'c,2;d,3',5],[int(1500*1.2),60,0,0,5,1800,None,5],[int(4800*1.2),120,0,3,13,4800,'b,2;c,2',5],[int(9000*1.2),0,100,4,24,9000,'c,2;d,3',5],[int(1500*1.3),60,0,0,5,1800,None,5],[int(4800*1.3),120,0,3,13,4800,'b,2;c,2',5],[int(9000*1.3),0,100,4,24,9000,'c,2;d,3',5],[7300,400,0,0,13,15840,None,10],[15000,0,150,4,21,24480,'f,2;g,2',10],[19000,0,-150,5,30,30600,'g,2;h,3',10],[int(7300*1.1),400,0,0,13,15840,None,10],[int(15000*1.1),0,150,4,21,24480,'f,2;g,2',10],[int(19000*1.1),0,-150,5,30,30600,'g,2;h,3',10],[int(7300*1.2),400,0,0,13,15840,None,10],[int(15000*1.2),0,150,4,21,24480,'f,2;g,2',10],[int(19000*1.2),0,-150,5,30,30600,'g,2;h,3',10],[int(7300*1.3),400,0,0,13,15840,None,10],[int(15000*1.3),0,150,4,21,24480,'f,2;g,2',10],[int(19000*1.3),0,-150,5,30,30600,'g,2;h,3',10],[3500,200,0,0,11,5400,None,15],[6600,0,120,5,25,11160,'d,2;e,2',15],[11000,0,-120,6,39,21240,'e,2;f,3',15],[int(3500*1.1),200,0,0,11,5400,None,15],[int(6600*1.1),0,120,5,25,11160,'d,2;e,2',15],[int(11000*1.1),0,-120,6,39,21240,'e,2;f,3',15],[int(3500*1.2),200,0,0,11,5400,None,15],[int(6600*1.2),0,120,5,25,11160,'d,2;e,2',15],[int(11000*1.2),0,-120,6,39,21240,'e,2;f,3',15],[int(3500*1.3),200,0,0,11,5400,None,15],[int(6600*1.3),0,120,5,25,11160,'d,2;e,2',15],[int(11000*1.3),0,-120,6,39,21240,'e,2;f,3',15],[10500,600,0,0,20,25200,None,20],[15500,0,200,7,32,36720,'h,2;i,2',20],[19500,0,-200,8,43,71640,'i,2;j,2',20],[int(10500*1.1),600,0,0,20,25200,None,20],[int(15500*1.1),0,200,7,32,36720,'h,2;i,2',20],[int(19500*1.1),0,-200,8,43,71640,'i,2;j,2',20],[int(10500*1.2),600,0,0,20,25200,None,20],[int(15500*1.2),0,200,7,32,36720,'h,2;i,2',20],[int(19500*1.2),0,-200,8,43,71640,'i,2;j,2',20],[int(10500*1.3),600,0,0,20,25200,None,20],[int(15500*1.3),0,200,7,32,36720,'h,2;i,2',20],[int(19500*1.3),0,-200,8,43,71640,'i,2;j,2',20],[-10,0,0,0,15,7560,None,5],[20000,0,300,12,25,15480,'b,2;c,2',5],[25000,0,-300,15,40,30600,'c,2;d,3',5],[int(-10*1.1),0,0,0,15,7560,None,5],[int(20000*1.1),0,300,12,25,15480,'b,2;c,2',5],[int(25000*1.1),0,-300,15,40,30600,'c,2;d,3',5],[int(-10*1.2),0,0,0,15,7560,None,5],[int(20000*1.2),0,300,12,25,15480,'b,2;c,2',5],[int(25000*1.2),0,-300,15,40,30600,'c,2;d,3',5],[int(-10*1.3),0,0,0,15,7560,None,5],[int(20000*1.3),0,300,12,25,15480,'b,2;c,2',5],[int(25000*1.3),0,-300,15,40,30600,'c,2;d,3',5],[-8,0,0,0,20,12240,None,3],[22000,0,310,15,30,19800,'a,2;f,2',3],[26000,0,-310,20,50,28800,'d,2;i,4',3],[int(-9),0,0,0,20,12240,None,3],[int(1.1*22000),0,310,15,30,19800,'a,2;f,2',3],[int(1.1*26000),0,-310,20,50,28800,'d,2;i,4',3],
[-2, 0, 0, 0, 10, 2*3600+1800, None, 2], [5500, 200, 0, 5, 15, 5*3600, "b,2;f,2", 2], [8000, 0, 100, 10, 30, 10*3600+360*3, "e,2;i,4", 2] 
]
resourcebuild=[[1000,0,80,0,5,0],[-10,0,0,0,15,10],[-15,0,0,0,40,20],[-20,0,0,0,70,30],[10000,600,120,0,20,10],[28500,1000,250,0,30,18]]

milbuild=[[4000,130,100,0,0,5,3600,None,1],[9000,0,20,200,5,10,11520,'a,3',1],[20000,0,50,-200,10,20,22680,'b,3;c,4',1],[12000,320,130,0,0,15,7200,None,5],[25000,0,20,500,7,20,14760,'b,3',5],[50000,0,50,-500,15,35,28440,'c,3;d,4',5],[6000,150,90,0,0,7,10800,None,5],[12000,0,20,300,3,15,21600,'c,3',5],[25000,0,50,-300,7,30,32400,'d,3;e,4',5], [20000, 400, 200, 0, 0, 20, 18000, None, 25], [45000, 0, 50, 400, 20, 50, 27000, 'a,8;b,8', 25], [100000, 0, 50, -400, 40, 100, 36000, 'c,15;g,15', 25]]
businessbuild=[[300,20,20,0,0,3,600,None,1],[500,30,5,0,1,7,1800,'a,1',1],[1100,0,10,70,2,11,3600,'a,2;b,3',1],[1200,45,40,0,0,5,3600,None,4],[1800,50,10,100,3,9,10740,'b,2;c,2',4],[3000,70,15,-100,4,14,15120,'c,2;d,3',4],[-5,0,0,0,0,15,5400,None,6],[5000,0,0,120,6,20,14400,'b,2;c,2',6],[7000,0,0,-120,7,25,23400,'c,2;d,3',6],[2000,80,50,0,0,7,19800,None,8],[3300,0,15,150,5,9,35270,'d,2;e,2',8],[4500,0,20,-150,6,11,46800,'e,2;f,3',8],[5000,100,70,0,0,9,8280,None,15],[7000,0,20,170,7,11,22320,'f,2;g,2',15],[13500,0,25,-170,8,13,28800,'g,2;h,3',15],[-8,0,0,0,0,25,20520,None,14],[9000,130,0,200,10,30,25200,'d,2;e,2',14],[11000,0,0,-200,11,35,33120,'e,2;f,3',14],[7200,130,90,0,0,20,21600,None,21],[11000,0,25,210,9,33,28800,'h,2;i,2',21],[19900,0,30,-210,10,45,36720,'i,2;j,3',21],[8000,170,110,0,0,29,30600,None,29],[13000,0,30,230,10,45,34200,'j,2;k,2',29],[21000,0,35,-230,11,61,46800,'k,2;l,3',29],[-11,0,0,0,0,35,25200,None,24],[13000,0,0,250,12,45,30240,'h,2;i,2',24],[17000,0,0,-250,13,60,39600,'i,2;j,3',24],[10000,1000,55,0,0,8,16200,None,7],[20000,0,18,300,7,15,28800,'a,5;i,4',7],[50000,0,27,-300,10,25,41400,'c,5;d,6',7],[10000,210,100,0,0,35,10*3600,None,35],[17000,280,30,280,10,47,11.5*3600,'d,4;h,6',35],[27000,-300,40,-300,11,56,13.5*3600,'g,5;a,10',35]]

godbuild=[[10000,500,0,50,100,7200],[10000,500,0,50,100,7200],[10000,500,0,50,100,7200],[10000,500,0,50,100,7200],[20000,1000,5,100,10,21600],[20000,1000,5,100,10,21600],[20000,1000,5,100,10,21600],[20000,1000,5,100,10,21600],[50000,2000,10,170,10,43200],[50000,2000,10,170,10,43200],[50000,2000,10,170,10,43200],[50000,2000,10,170,10,43200],[100000,5000,15,250,10,64800],[100000,5000,15,250,10,64800],[100000,5000,15,250,10,64800],[100000,5000,15,250,10,64800],[500000,10000,30,350,10,86400],[500000,10000,30,350,10,86400],[500000,10000,30,350,10,86400],[500000,10000,30,350,10,86400]]

statuebuilding = [[12,80000,600,10,7200],[12,-8,700,10,14400],[13,120000,950,10,21600],[13,-12,1200,10,28800],[15,200000,1600,10,36000],[15,-20,2500,10,43200]]
#corn person level
decorationbuild=[[10,5,1],[20,5,1],[30,5,1],[50,5,4],[-1,50,5],[100,6,6],[100,6,6],[100,6,6],[100,6,6],[100,6,6],[100,6,6],[200,8,7],[-3,170,8],[400,15,9],[600,20,10],[800,25,11],[1000,30,12],[900,35,13],[1200,40,14],[2000,50,15],[-5,300,10],[1500,60,16],[1500,60,16],[1500,60,16],[1600,65,18],[1600,65,18],[1600,65,18],[1600,65,18],[-3,150,15],[-3,150,15],[-3,150,15],[-3,150,15],[1800,70,20],[1800,70,20],[1800,70,20],[2000,80,25],[2000,80,25],[2000,80,25],[-10,300,20],[5000,90,3],[-5,150,3],[-10,300,3],[2000,30,17],[2000,30,17],[-10,300,20],[-2,120,30],[-5,150,40],[-6,155,40],[-7,160,40],[-8,165,40],[-88,-2,25],[-50,-1,10],[5000,90,6],[-45,-1,8],[5000,90,6],[5000,90,15],[-45,-1,20],[100,10,3],[-40,-1,5],[-42,-1,7],[10000,130,7],[-46,-1,20],[5500,100,30], 
[-5, 150, 3], [900, 30, 5], [-40, -1, 6], [-2, 100, 8] ]

def buildGod(user, city_id, ground_id, grid_id, bid, eid):
    curTime=int(time.mktime(time.localtime())-time.mktime(beginTime))
    if ground_id >= bid and ground_id <= eid:
        buildings = DBSession.query(businessWrite).filter("city_id=:cid and ground_id >= :bid and  ground_id <= :eid").params(cid=city_id, bid=bid, eid=eid).all()
        if len(buildings) != 0:
            return dict(id=0, reason=" god exists in city")
        lev = int(ground_id)-420
        if lev == 0:
            if user.lev < 25:
                return dict(id=0, reason="level < 25")
        if lev == 5:
            if user.lev < 30:
                return dict(id=0, reason="level < 30")
        lev = lev%5
        if user.food >= friendGod[lev][1] and user.corn >= friendGod[lev][2]:
            user.food -= friendGod[lev][1]
            user.corn -= friendGod[lev][2]
            user.populationupbound += friendGod[lev][4]
            user.exp += friendGod[lev][3]

            building = businessKeep(city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 0)
            DBSession.add(building)
            DBSession.flush()

            building = businessWrite(bid = building.bid, city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 0)
            DBSession.add(building)
            print "buildGod", friendGod[lev][1], friendGod[lev][2]
            return dict(id=1, result="friendgod or monster god  suc")
        else:
            return dict(id=0, reason="resource not enough")
    return dict(id=0, reason="unknown")

def buildDecoration(user, city_id, ground_id, grid_id):
    index = ground_id%100
    coinCost = 0
    caeCost = 0
    popAdd = 0
    boundAdd = 0
    cost = decorationbuild[index]
    if cost[0] > 0:
        coinCost = cost[0]
    else:
        caeCost = -cost[0]
    if cost[1] > 0:
        popAdd = cost[1]
    else:
        boundAdd = -cost[1]
    print inspect.stack()[0]
    if user.corn >= coinCost and user.cae >= caeCost:
        user.corn -= coinCost
        user.cae -= caeCost
        user.populationupbound += popAdd
        m = DBSession.query(Mana).filter_by(userid=user.userid).one()
        m.boundary += boundAdd
        building = businessKeep(city_id = city_id, ground_id=ground_id, grid_id=grid_id, object_id = -1, producttime = 0, finish = 1)
        DBSession.add(building)
        DBSession.flush()

        building = businessWrite(bid = building.bid, city_id = city_id, ground_id=ground_id, grid_id=grid_id, object_id = -1, producttime = 0, finish = 1)
        DBSession.add(building)
        print "buildDecoration", coinCost, caeCost
        return dict(id=1)
    return dict(id=0)


def buildDragon(user, city_id, ground_id, grid_id):
    print "dragon", user.food, user.corn
    if ground_id == 1000:
        if user.food >= DraDemand[1] and user.corn >= DraDemand[2]:
            print "check dragon"
            
            existDragon = DBSession.query(businessWrite).filter_by(city_id=city_id).filter_by(ground_id=ground_id).all()
            if len(existDragon) != 0:
                return dict(id=0, reason="dragon exist")
            
            building = businessKeep(city_id = city_id, ground_id=ground_id, grid_id=grid_id, object_id = -1, producttime = 0, finish = 1)
            DBSession.add(building)
            DBSession.flush()

            building = businessWrite(bid=building.bid, city_id = city_id, ground_id=ground_id, grid_id=grid_id, object_id = -1, producttime = 0, finish = 1)
            DBSession.add(building)
            DBSession.flush()
            
            user.food -= DraDemand[1]
            user.corn -= DraDemand[2]
            user.populationupbound += 100

            dragon = Dragon(uid = user.userid, bid = building.bid, friNum = 0, state=0,  health = 0, name = 'My Pet', kind = 0, friList= '[]', lastFeed = 0, trainNum = 0, attack=0)
            DBSession.add(dragon)
            return dict(id=1, result = "build dragon suc")
    return dict(id = 0, reason = "dragon fail lev or food or corn need")
def buildStatue(user, city_id, ground_id, grid_id):
    curTime=int(time.mktime(time.localtime())-time.mktime(beginTime))
    index = ground_id%600
    idlepop = user.population - user.labor_num
    coinCost = 0
    caeCost = 0
    if statuebuilding[index][1] > 0:
        coinCost = statuebuilding[index][1]
    else:
        caeCost = -statuebuilding[index][1]
    if user.lev >= statuebuilding[index][0] and idlepop >= statuebuilding[index][3] and user.cae >= caeCost and user.corn >= coinCost:
        statue = businessKeep(city_id = city_id, ground_id=ground_id, grid_id=grid_id, object_id = -1, producttime = curTime, finish = 0)
        DBSession.add(statue)
        DBSession.flush()

        statue = businessWrite(bid = statue.bid, city_id = city_id, ground_id=ground_id, grid_id=grid_id, object_id = -1, producttime = curTime, finish = 0)
        DBSession.add(statue)
        user.cae -= caeCost
        user.corn -= coinCost
        user.labor_num += statuebuilding[index][3]
        user.defencepower += statuebuilding[index][2]
        return dict(id=1,result = "build statue suc")
    else:
        return dict(id=0,reason = "statue lev or pop failed")
#time food coin exp personMax caecost
def buildNormalGod(user, city_id, ground_id, grid_id):
    curTime=int(time.mktime(time.localtime())-time.mktime(beginTime))
    buildings = DBSession.query(businessWrite).filter("city_id=:cid and ground_id >= :bid and  ground_id <= :eid and (ground_id%400)%4 = :gid ").params(cid=city_id, bid=400, eid=419, gid=((ground_id%400)%4)).all()
    if len(buildings) > 0:
        return dict(id=0, reason="god exist")
    lev = (ground_id%400)/4
    cost = friendGod[lev]
    if user.food >= friendGod[lev][1] and user.corn >= friendGod[lev][2]:
        user.food -= friendGod[lev][1]
        user.corn -= friendGod[lev][2]
        user.populationupbound += friendGod[lev][4]
        user.exp += friendGod[lev][3]
        building = businessKeep(city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 0)
        DBSession.add(building)
        DBSession.flush()

        building = businessWrite(bid = building.bid, city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 0)
        DBSession.add(building)
        print "buildGod", cost[2], cost[1]
        return dict(id=1, result="normal god  suc")
    return dict(id=0, reason="nor god resource not enough")
    


#coin food wood caesars exp buildTime specials size 
def buildRoom(user, city_id, ground_id, grid_id):
    curTime=int(time.mktime(time.localtime())-time.mktime(beginTime))
    index = ground_id%100
    if index % 3 != 0:
        return dict(id=0, reason="can not upgrade")
    cost = housebuild[index]
    coinCost = 0
    caeCost = 0
    if cost[0] > 0:
        coinCost = cost[0]
    else:
        caeCost = -cost[0]
    if user.corn >= coinCost and user.food >= cost[1] and user.cae >= caeCost:
        user.corn -= coinCost
        user.food -= cost[1]
        user.cae -= caeCost
        user.exp += cost[4]
        building = businessKeep(city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 0)
        DBSession.add(building)
        DBSession.flush()
        building = businessWrite(bid = building.bid, city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 0)
        DBSession.add(building)
        print "buildRoom", coinCost, caeCost, cost[1]
        return dict(id=1, result="room suc")
    return dict(id=0, reason = 'fail')

#coin food person wood cae exp time spe level 
#coin food person wood cae bexp time spe level
def buildBusiness(user, city_id, ground_id, grid_id):
    curTime=int(time.mktime(time.localtime())-time.mktime(beginTime))
    index = ground_id%100
    if index % 3 != 0:
        return dict(id=0, reason="can not upgrade")
    if ground_id >= 300:
        cost = businessbuild[index]
    else:
        cost = milbuild[index]
    coinCost = 0
    caeCost = 0
    if cost[0] > 0:
        coinCost = cost[0]
    else:
        caeCost = -cost[0]
    if user.corn >= coinCost and user.food >= cost[1] and (user.population-user.labor_num) >= cost[2]:
        user.corn -= coinCost
        user.food -= cost[1]
        user.labor_num += cost[2]
        user.cae -= caeCost
        user.exp += cost[5]
        building = businessKeep(city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 0)
        DBSession.add(building)
        DBSession.flush()

        building = businessWrite(bid=building.bid, city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 0)
        DBSession.add(building)
        print "buildBusiness", coinCost, caeCost, cost[1], cost[2]
        return dict(id=1, result="business/mil suc")
    return dict(id=0, reason = 'business/mil fail')
    
#coin food person 0 exp lev 
#resourcebuild=[[1000,0,80,0,5,0],[-10,0,0,0,15,10],[-15,0,0,0,40,20],[-20,0,0,0,70,30],[10000,600,120,0,20,10],[28500,1000,250,0,30,18]]
def buildFarm(user, city_id, ground_id, grid_id):
    curTime=int(time.mktime(time.localtime())-time.mktime(beginTime))
    index = ground_id%100-1
    cost = resourcebuild[index]
    coinCost = 0
    caeCost = 0
    if cost[0] > 0:
        coinCost = cost[0]
    else:
        caeCost = -cost[0]
    if user.corn >= coinCost and user.food >= cost[1] and (user.population-user.labor_num) >= cost[2]:
        user.corn -= coinCost
        user.food -= cost[1]
        user.labor_num += cost[2]
        user.cae -= caeCost
        user.exp += cost[4]
        building = businessKeep(city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 1)
        DBSession.add(building)
        DBSession.flush()

        building = businessWrite(bid = building.bid, city_id=city_id, ground_id=ground_id, grid_id=grid_id, object_id=-1, producttime = curTime, finish = 1)
        DBSession.add(building)
        print "buildFarm", coinCost, caeCost, cost[1], cost[2] 
        return dict(id=1, result="farm suc")
    return dict(id=0, reason = 'farm fail')

#coin person lev

def buildDisk(user, city_id, ground_id, grid_id):
    curTime=int(time.mktime(time.localtime())-time.mktime(beginTime))
    if user.corn >= DiskBuild[0]:
        building = businessKeep(city_id = city_id, ground_id=ground_id, grid_id=grid_id, object_id = -1, producttime = curTime, finish = 0)
        DBSession.add(building)
        DBSession.flush()

        building = businessWrite(bid = building.bid, city_id = city_id, ground_id=ground_id, grid_id=grid_id, object_id = -1, producttime = curTime, finish = 0)
        DBSession.add(building)
        user.corn -= DiskBuild[0]
        user.populationupbound += DiskBuild[1]
        DBSession.flush()
        return dict(id=1)
    return dict(id=0, reason='money not enough')
