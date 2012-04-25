# -*- coding: utf-8 -*-
"""Fallback controller."""


from tg import expose, flash, require, url, request, redirect,response
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from pylons import response
from repoze.what import predicates

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import or_, and_, desc, select
from sqlalchemy import func

from stchong.lib.base import BaseController

from stchong.model import DBSession, db 
import random
from stchong import model
import json
from stchong.controllers.util import *
import inspect
import time

import time


        

__all__ = ['GoodsController']

#goods
#dragonStone
#0
class GoodsController(BaseController):
    #[[oid, num]]
    #0 - 8
    global Possible
    Possible = [
    [1, 30, 200, 50, 100, 200, 200, 200, 19],
    [10, 4, 1, 10, 20, 20, 15, 10, 10],
    [200, 50, 9, 40, 200, 200, 100, 200, 1]
    ]
    def getReward(self, user, kind, diskType):
        if diskType == 0:
            if kind == 0:
                mana = DBSession.query(model.Mana).filter_by(userid=user.userid).one()
                mana.boundary += 1
            elif kind == 1:
                user.cae += 9
            elif kind == 2:
                user.food += 99
            elif kind == 3:
                spe = getSpecial(user)
                spe[0][1] += 1
                setUserSpe(user.userid, setSpecial(spe))
                #user.specialgoods = setSpecial(spe)
            elif kind == 4:
                user.corn += 999
            elif kind == 5:
                changeGoods(user.userid, 0, 1)
            elif kind == 6:
                user.food += 999
            elif kind == 7:
                user.cae += 1
            elif kind == 8:
                user.corn += 9999
        elif diskType == 1:
            if kind == 0:
                user.corn += 99
            elif kind == 1:
                user.food += 999
            elif kind == 2:
                user.infantrypower += 999
            elif kind == 3:
                user.corn += 9
            elif kind == 4:
                user.food += 99
            elif kind == 5:
                user.infantrypower += 9
            elif kind == 6:
                user.corn += 999
            elif kind == 7:
                user.food += 9
            elif kind == 8:
                user.infantrypower += 99
        else:
            if kind == 0:
                user.corn += 99
            elif kind == 1:
                user.food += 999
            elif kind == 2:
                user.cae += 9
            elif kind == 3:
                user.corn += 9999
            elif kind == 4:
                user.food += 99
            elif kind == 5:
                user.cae += 1
            elif kind == 6:
                user.corn += 999
            elif kind == 7:
                user.food += 9
            elif kind == 8:
                user.cae += 99

        
    @expose('json')
    def startDragon(self, uid, kind):
        kind = int(kind)
        uid = int(uid)
        diskType = kind/1000
        kind = kind % 1000
        user = getUser(uid)
        ok = False
        if kind == 0:
            goods = getGoods(uid).get('goods')
            stone = goods.get(str(0), 0)
            #print goods, stone
            if stone >= 1:
                ok = True
                changeGoods(uid, 0, -1)
            print "startDragon", uid, kind, time.mktime(time.localtime())
        else:
            if user.cae >= 1:
                ok = True
                user.cae -= 1
            print "startDragon", uid, kind, time.mktime(time.localtime())

        if ok:
            all = sum(Possible[diskType])
            v = random.randint(0, all-1)            
            last = 0
            for i in range(len(Possible[diskType])):
                cur = sum(Possible[diskType][:i+1])
                if v >= last and v < cur:
                    break
                last = cur
            self.getReward(user, i, diskType)
            print "dragonReward", uid, i
            return dict(id=1, result=i)
        return dict(id=0, reason = "stone or cae not enough")

    #0 normal 1 cae 2 battle 
    """
    @expose('json')
    def startDragon(self, uid, kind):
        kind = int(kind)
        uid = int(uid)
        ok = False
        user = getUser(uid)
        if kind == 0:
            goods = getGoods(uid).get('goods')

            stone = goods.get(str(0), 0)
            #print goods, stone
            if stone >= 1:
                ok = True
                changeGoods(uid, 0, -1)
            print "startDragon", uid, kind, time.mktime(time.localtime())
        else:
            if user.cae >= 1:
                ok = True
                user.cae -= 1
            print "startDragon", uid, kind, time.mktime(time.localtime())
        if ok:
            all = sum(Possible)
            v = random.randint(0, all-1)            
            last = 0
            for i in range(len(Possible)):
                cur = sum(Possible[:i+1])
                if v >= last and v < cur:
                    break
                last = cur
            self.getReward(user, i)
            print "dragonReward", uid, i
            return dict(id=1, result=i)
        return dict(id=0, reason = "stone or cae not enough")
    """     
