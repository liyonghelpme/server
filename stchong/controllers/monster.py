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
from stchong.model import Monster, MonsterResult
import inspect
import time



        

__all__ = ['MonsterController']

class MonsterController(BaseController):
    @expose('json')
    def getMyResult(self, uid):
        return getResult(uid)
    #@expose('json')
        
        
    @expose('json')
    def attackMonster(self, uid, monsterId, inf, cav, cata):
        uid = int(uid)
        monsterId = int(monsterId)
        inf = int(inf)
        cav = int(cav)
        cata = int(cata)
        try:
            monster = DBSession.query(Monster).filter_by(id=monsterId).one()
        except:
            return dict(id=0, reason='no such monster', status = 0)
        user = getUser(uid)
        if user.infantrypower < inf or user.cavalrypower < cav or  user.catapult < cata or inf < 0 or cav < 0 or cata < 0:
            return dict(id=0, reason='solder not ', status = 1)
        curPower = monster.power
        returnInf = inf - curPower
        returnCav = cav + min(returnInf, 0)
        returnCata = cata + min(returnCav, 0)

        returnInf = max(returnInf, 0)
        returnCav = max(returnCav, 0)
        returnCata = max(returnCata, 0)

        lostInf = inf - returnInf
        lostCav = cav - returnCav
        lostCata = cata - returnCata

        lostPower = lostInf+lostCav+lostCata
        leftPower = curPower - lostPower

        try:
            attacker = json.loads(monster.attacker)
        except:
            attacker = []
        find = False
        for i in attacker:
            if i[0] == uid:
                i[1] += lostPower
                find = True
                break
        if find == False:
            attacker.append([uid, lostPower])
        monster.attacker = json.dumps(attacker)
        monster.power = leftPower


        user.infantrypower -= lostInf
        user.cavalrypower -= lostCav
        user.catapult -= lostCata

        if leftPower <= 0:
            calResult(monster)
            DBSession.delete(monster)
            
        return dict(id=1, lostInf = lostInf, lostCav = lostCav, lostCata = lostCata, leftPower = leftPower)
            





