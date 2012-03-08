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

import time


        

__all__ = ['GroupController']

#goods
#dragonStone
#0
class GroupController(BaseController):
    global itsMap
    def itsMap(uid):
        myMap = db.map.findOne({'uid':uid})
        allUser = db.map.find({'mid':myMap['mid']})
        res = []
        for u in allUser:
            res.append([u['uid'], u['sid'], u['gid']])
        return dict(id=1, mid=myMap['mid'], mapData = res)

    @expose('json')
    def enterWar(self, uid):
        cur = getNow()
        uid = int(uid)
        inMap = db.map.find_one({'uid':uid})
        if inMap:
            return itsMap(uid)

        war = db.war.find_one({'count': {'$lt':10}}) 
        if war == None:
            war = {'id':cur, 'count':0}
            exist = db.war.find_one({'id':cur})
            if not exist:
                db.war.insert(war)
            else:
                return dict(id=0, reason='create New Map fail')

        war['count'] += 1
        allUser = db.map.find({'mid':war['id']})
        sides = {'left':[], 'right':[]}
        for a in allUser:
            if a['sid'] == 0:
                sides['left'].append(a['gid'])
            else:
                sides['right'].append(a['gid'])
        sid = 0
        gids = sides['left']
        if len(sides['left']) > len(sides['right']):
            sid = 1
            gids = sides['right']
        gid = len(gids)
        db.map.insert({'uid': uid, 'mid':war['id'], 'sid': sid, 'gid': gid, 'soldiers':[0, 0, 0], 'readTime': cur})

        db.war.save(war)
        return itsMap(uid)
    @expose('json')
    def groupAttack(self, uid, mid, fgid, tgid, soldiers, timeNeed):
        uid = int(uid)
        mid = int(mid)
        fgid = int(fgid)
        tgid = int(tgid)
        soldiers = json.loads(soldiers)
        timeNeed = int(timeNeed)

        cur = getNow()
        fc = db.castal.find_one({'mid':mid, 'gid':fgid, 'uid':uid})
        if fc == None:
            return dict(id=0, status =1, reason='no soldiers')
        #tc = db.castal.find_one({'mid':mid, 'gid':tgid})
        fsoldiers = fc['soldiers']
        i = 0
        while i < len(soldiers):
            if fsoldiers[i] < soldiers[i]:
                return dict(id=0, statue=0, reason='soldier not enough')
            i += 1
        i = 0
        while i < len(soldiers):
            fsoldiers[i] -= soldiers[i]
            i += 1
        
        battle = {'mid':mid , 'uid':uid,  'fgid':fgid, 'tgid':tgid, 'soldiers':soldiers, 'timeLeft':cur, 'timeNeed':timeNeed}
        db.battle.insert(battle)
        db.castal.save(fc)
        return dict(id=1)

    global calBattle
    def calBattle():
        cur = getNow()
        battles = db.battle.find()
        for b in battles:
            passTime = cur - b['timeLeft']
            if passTime > b['timeNeed']:
                user = db.map.findOne({'uid':b['uid']})
                defCastal = db.castal.find({'mid':b['mid'], 'gid':b['tgid']})
                #lost less 10% cityNum occupy by who? nearBy will show ti
                attPow = sum(b['soldiers'])
                defSoldier = 0
                for d in defCastal:
                    defSoldier += sum(d['soldiers'])
                if attPow > defSoldier:
                    lost = min(attPow/10, defSoldier/10)*1.0
                    attLost = lost
                    defLost = min(lost+defSoldier/20, defSoldier)
                else:
                    lost = min(attPow/10, defSoldier/10)*1.0
                    attLost = min(lost+attPow/20, attPow)
                    defLost = lost
                #not zero
                attRate = attLost/attPow
                #not zero
                if defSoldier > 0:
                    defRate = defLost/defSoldier
                else:
                    defRate = 1
                b['soldiers'][0] *= (1-attRate)
                b['soldiers'][1] *= (1-attRate)
                b['soldiers'][2] *= (1-attRate)
                db.battle.remove(b)
                if attPow > defSoldier:
                    db.castal.insert({'mid':b['mid'], 'gid':b['tgid'], 'uid':b['uid'], 'soldiers':b['soldiers'] })
                else:
                    attUser = db.map.findOne({'uid':b['uid']})


                for d in defCastal:
                    d['soldiers'][0] *= (1-defRate)
                    d['soldiers'][1] *= (1-defRate)
                    d['soldiers'][2] *= (1-defRate)
                    db.battleresult.insert({'mid':b['mid'], 'uid':b['uid'], 'defid':d['uid'], 'fgid':b['fgid'], 'tgid':b['tgid'], 'soldiers':b['soldiers'], 'calTime':cur, 'defSoldier':d['soldiers'],  'attRate':attRate, 'defRate':defRate} )
                    if attPow > defSoldier:
                        defUser = db.map.findOne({'uid':d['uid']})
                        defUser['soldiers'][0] += d['soldiers'][0]
                        defUser['soldiers'][1] += d['soldiers'][1]
                        defUser['soldiers'][1] += d['soldiers'][1]
                        db.map.save(defUser)
                        db.castal.remove(d)
                    else:
                        db.castal.save(d)
        


                    

                    
                



                
