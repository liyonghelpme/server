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
from stchong.model import MyMonster
import inspect
import time



        

__all__ = ['MyMonsterController']

class MyMonsterController(BaseController):
    global MON_DRA
    MON_DRA = 50
    global MAX_MON
    MAX_MON = 10
    global MON_CAE
    MON_CAE = 100
    global MON_ID
    MON_ID = range(18, 36)
    def genNewMonster(self, user):
        #mid kindid power
        maxId = -1
        monsters = json.loads(user.monsters)
        for i in monsters:
            if i[0] > maxId:
                maxId = i[0]
        maxId += 1
        gids = [g[3] for g in monsters]
        leftGids = list(set(range(0, 10))-set(gids))
        print "leftGids", leftGids
        hasSpe = False
        for i in monsters:
            if i[4] == 1:
                hasSpe = True
                break
        if not hasSpe:
            kindId = random.randint(0, len(MON_ID)-1)
            kindId = MON_ID[kindId]
            power = 80+4*user.waveNum//8
            monsters.append([maxId, kindId, power, leftGids[0], 1])
            leftGids.pop(0)
            maxId += 1
        print "monsters", monsters
            
        for i in range(0, MAX_MON - len(monsters)):
            kindId = random.randint(0, len(MON_ID)-1)
            kindId = MON_ID[kindId]
            power = 40+2*user.waveNum//8
            monsters.append([maxId, kindId, power, leftGids[i], 0])
            maxId += 1
        user.monsters = json.dumps(monsters)
            
        
        
    def getMyMonster(self, uid):
        uid = int(uid)
        try:
            user = DBSession.query(MyMonster).filter_by(uid = uid).one()
        except:
            user = MyMonster(uid=uid, monsters='[]', lastTime = 0)
            DBSession.add(user)
            DBSession.flush()
        curTime = getTime()
        dif = curTime - user.lastTime
        if dif >= 3600*2:
            monsters = json.loads(user.monsters)
            if len(monsters) < MAX_MON:
                self.genNewMonster(user)
                user.lastTime = curTime
        return user
    @expose('json')
    def getMonsters(self, uid):
        uid = int(uid)
        user = self.getMyMonster(uid)
        return dict(id=1, monsters=json.loads(user.monsters))
            
    @expose('json')
    def attackMonster(self, uid, mid, kind):
        print "killMonster", uid, mid, kind
        uid = int(uid)
        mid = int(mid)
        kind = int(kind)

        user = getUser(uid)

        mon = self.getMyMonster(uid)
        ms = json.loads(mon.monsters)
        find = False
        for i in ms:
            if i[0] == mid:
                find = True                
                break
        if find:
            print "killMon", i
            power = i[2]
            if kind == 0:#attack with cae
                cost = (power+MON_CAE-1)/MON_CAE
                if cost > user.cae:
                    return dict(id=0, reason='cae not', status = 2)
                user.cae -= cost
            else:
                if user.infantrypower+user.cavalrypower+user.catapult < power:
                    return dict(id=0, status = 0, reason='soldier not')

                inf = user.infantrypower
                cav = user.cavalrypower
                cata = user.catapult

                returnInf = inf - power
                returnCav = cav + min(returnInf, 0)
                returnCata = cata + min(returnCav, 0)

                returnInf = max(returnInf, 0)
                returnCav = max(returnCav, 0)
                returnCata = max(returnCata, 0)

                lostInf = inf - returnInf
                lostCav = cav - returnCav
                lostCata = cata - returnCata

                user.infantrypower = returnInf
                user.cavalrypower = returnCav
                user.catapult = returnCata

            ms.remove(i)
            mon.monsters = json.dumps(ms)
            mon.waveNum = min(mon.waveNum+1, 250*8)
            dragonNum = (power+MON_DRA-1)//MON_DRA;
            changeGoods(uid, 0, dragonNum)
            changeMonRank(uid)
            if kind == 0:
                return dict(id=1, caeCost = cost, dragonNum = dragonNum)
            else:
                return dict(id=1, lostInf=lostInf, lostCav=lostCav, lostCata=lostCata, dragonNum = dragonNum)
        return dict(id=0, status = 1, reason='no monster find')

