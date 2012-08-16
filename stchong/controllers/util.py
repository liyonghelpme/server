# -*- coding: utf-8 -*-
"""Fallback controller."""

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import or_, and_, desc, select
from sqlalchemy import func


from stchong.model import DBSession, db 
import random
from stchong import model
from stchong.model import WarRes, operationalData, Spe, Ship
import json
import time
from stchong.model import Monster, MonsterResult

beginTime=(2011,1,1,0,0,0,0,0,0)
def getTime():
    curTime = int(time.mktime(time.localtime())-time.mktime(beginTime))
    return curTime
def getShip(uid):
    try:
        ship = DBSession.query(Ship).filter_by(uid=uid).one()
    except:
        ship = Ship(uid=uid, sid = 0, state = -1, startTime = 0, timeNeed = 0, goodsKind = 0, num = 0)
        DBSession.add(ship)
        DBSession.flush()
    return ship
def returnShip(uid):
    ship = getShip(uid)
    return [ship.state, ship.startTime, ship.timeNeed, ship.goodsKind, ship.num]

def getUserSpe(uid):
    try:
        spe = DBSession.query(Spe).filter_by(uid=uid).one()
    except:
        user = getUser(uid)
        spe = Spe(uid=uid, specialgoods=user.specialgoods)
        DBSession.add(spe)
        DBSession.flush()
    return spe.specialgoods
def setUserSpe(uid, s):
    try:
        spe = DBSession.query(Spe).filter_by(uid=uid).one()
    except:
        user = getUser(uid)
        spe = Spe(uid=uid, specialgoods=user.specialgoods)
        DBSession.add(spe)
        DBSession.flush()
    spe.specialgoods = s


def getSpecial(user):
    spe = getUserSpe(user.userid).split(';')
    #spe = user.specialgoods.split(";")
    res = []
    for s in spe:
        s = s.split(',')
        res.append([s[0], int(s[1])])
    return res
def setSpecial(spe):
    res = ""
    i = 0
    for s in spe:
        if i == 0:
            res += s[0]+','+str(s[1])
            i += 1
        else:
            res += ';'+s[0]+','+str(s[1])
    return res

def checkSpe(cost, spe):
    for i in cost:
        pos = int(i[0], 36)- int('a', 36)
        if spe[pos][1] < i[1]:
            return False
    return True
def costSpe(cost, spe):
    for i in cost:
        pos = int(i[0], 36)- int('a', 36)
        spe[pos][1] -= i[1]
    return spe 

def getUser(uid):
    user = DBSession.query(operationalData).filter_by(userid=uid).one()
    return user


#{uid, {str(oid):num, str(oid): num}}
def getGoods(uid):
    goods = db.goods.find_one({'uid':uid}) 
    if goods == None:
        db.goods.insert({'uid':uid, 'goods':{str(0): 1}})
        goods = db.goods.find_one({'uid':uid}) 
    return goods
def changeGoods(uid, kind, num):
    goods = getGoods(uid)
    objs = goods['goods']
    kind = str(kind)
    g = objs.get(kind)
    if g == None:
        objs[kind] = num
    else:
        objs[kind] += num
    db.goods.update({'uid':uid}, {'$set': {'goods': objs}})

def getBattleRes(uid):
    try:
        res = DBSession.query(WarRes).filter_by(uid=uid).one()
    except:
        user = getUser(uid)
        res = WarRes(uid=uid, battleresult=user.battleresult, nbattleresult=user.nbattleresult)
        DBSession.add(res)
        DBSession.flush()
    try:
        res = json.loads(res.battleresult)
    except:
        res = []
    return res
def setBattleRes(uid, bat):
    bat = json.dumps(bat)
    try:
        res = DBSession.query(WarRes).filter_by(uid=uid).one()
    except:
        user = getUser(uid)
        res = WarRes(uid=uid, battleresult=user.battleresult, nbattleresult=user.nbattleresult)
        DBSession.add(res)
        DBSession.flush()

    res.battleresult = bat
    

def getNBattleRes(uid):
    try:
        res = DBSession.query(WarRes).filter_by(uid=uid).one()
    except:
        user = getUser(uid)
        res = WarRes(uid=uid, battleresult=user.battleresult, nbattleresult=user.nbattleresult)
        DBSession.add(res)
        DBSession.flush()
    try:
        res = json.loads(res.nbattleresult)
    except:
        res = []
    return res
def setNBattleRes(uid, bat):
    bat = json.dumps(bat)
    try:
        res = DBSession.query(WarRes).filter_by(uid=uid).one()
    except:
        user = getUser(uid)
        res = WarRes(uid=uid, battleresult=user.battleresult, nbattleresult=user.nbattleresult)
        DBSession.add(res)
        DBSession.flush()

    res.nbattleresult = bat



def getMonster(uid, mid):
    uid = int(uid)
    mid = int(mid)
    monster = DBSession.query(Monster).filter_by(mid=mid).all()
    return dict(id=1, monster=monster)
def calResult(monster):
    attacker = json.loads(monster.attacker)
    totalPower = sum([i[1] for i in attacker])
    dragonNum = monster.dragonNum
    for i in attacker:
        reward = dragonNum*i[1]/totalPower
        monR = MonsterResult(uid=i[0], mid=monster.id, dragonNum=reward, power = i[1], totalNum = totalPower, readYet = 0)
        #changeGoods(i[1], 0, reward )
        try:
            exis = DBSession.query(MonsterResult).filter_by(uid=i[0]).filter_by(mid=monster.id).one()
            exis.readYet = 0
            exis.dragonNum += reward
            exis.power += i[1]
        except:
            DBSession.add(monR)

def getResult(uid):
    uid = int(uid)
    res = DBSession.query(MonsterResult).filter_by(uid=uid).filter_by(readYet = 0).all()
    user = getUser(uid)
    for r in res:
        r.readYet = 1
        changeGoods(uid, 0, r.dragonNum)
    print "monster Result", res

    return dict(id=1, res=res)

    

def changeMonRank(uid):
    act = db.rank.find_one({'uid':uid})
    if act == None:
        db.rank.save({'uid':uid, 'mon':0, 'order':1000})
        db.rank.ensure_index("uid")
        act = db.rank.find_one({'uid':uid})
    mNum = act.get('mon', 0)
    act['mon'] = mNum+1
    db.rank.save(act)
