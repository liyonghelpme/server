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
        if kind == 0:
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
    goods = getGoods(uid)
    objs = goods['goods']
    kind = str(kind)
    g = objs.get(kind)
    if g == None:
        objs[kind] = 1
    else:
        objs[kind] += 1
    db.goods.update({'uid':uid}, {'$set': {'goods': objs}})

