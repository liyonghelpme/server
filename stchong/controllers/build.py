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
