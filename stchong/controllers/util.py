# -*- coding: utf-8 -*-
"""Fallback controller."""

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import or_, and_, desc, select
from sqlalchemy import func


from stchong.model import DBSession, db 
import random
from stchong import model
from stchong.model import warMap
import json
from stchong.model import Monster, MonsterResult


def getSpecial(user):
    spe = user.specialgoods.split(";")
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
    user = DBSession.query(model.operationalData).filter_by(userid=uid).one()
    return user


#{uid, {str(oid):num, str(oid): num}}
def getGoods(uid):
    goods = db.goods.find_one({'uid':uid}) 
    if goods == None:
        db.goods.insert({'uid':uid, 'goods':{str(0): 1}})
        goods = db.goods.find_one({'uid':uid}) 
    return goods
def changeGoods(uid, kind, num):
    print "changeGoods", uid, kind, num
    goods = getGoods(uid)
    objs = goods['goods']
    kind = str(kind)
    g = objs.get(kind)
    if g == None:
        objs[kind] = num
    else:
        objs[kind] += num
    db.goods.update({'uid':uid}, {'$set': {'goods': objs}})

def getMinusState(minus):
    try:
        mlist = json.loads(minus)
    except:
        mlist = []
    s = ''
    i = 0
    for m in mlist:
        if i == 0:
            s += str(m[0])+','+str(m[1])
            i += 1
        else:
            s += ';'+str(m[0])+','+str(m[1])
    return s


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

    return dict(id=0, res=res)
