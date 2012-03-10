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
import math

        

__all__ = ['GroupController']

#goods
#dragonStone
#0
class GroupController(BaseController):
    global ProtectTime
    ProtectTime = 0
    global itsMap
    def itsMap(uid):
        cur = getNow()
        myMap = db.map.find_one({'uid':uid})
        allUser = db.map.find({'mid':myMap['mid']})
        userNum = db.map.find({'mid':myMap['mid']}).count()
        war = db.war.find_one({'mid':myMap['mid']})
        if userNum >= 10:
            if war['startTime'] == -1:
                war['startTime'] = cur
                db.war.save(war)
                castal = db.castal.find({'mid':war['mid']})
                for c in castal:
                    c['protectTime'] = cur+ProtectTime
                    db.castal.save(c)
        res = []
        for u in allUser:
            res.append([u['uid'], u['sid'], u['gid']])
        return dict(id=1, mid=myMap['mid'], mapData = res, startTime = war['startTime'])

    @expose('json')
    def checkInMap(self, uid):
        uid = int(uid)
        user = db.map.find_one({'uid':uid})
        if user == None:
            return dict(id=1, mid=-1)
        return dict(id=1, mid=user['mid'])

    @expose('json')
    def enterWar(self, uid):
        cur = getNow()
        uid = int(uid)
        inMap = db.map.find_one({'uid':uid})
        if inMap:
            return itsMap(uid)

        war = db.war.find_one({'count': {'$lt':10}}) 
        if war == None:
            war = {'mid':cur, 'count':0, 'startTime':-1, 'left':0, 'right':0, 'finish':0}
            exist = db.war.find_one({'mid':cur})
            if not exist:
                db.war.insert(war)
                war = db.war.find_one({'mid': cur})
            else:
                return dict(id=0, reason='create New Map fail')

        war['count'] += 1
        db.war.save(war)

        allUser = db.map.find({'mid':war['mid']})
        sides = {'left':0, 'right':0}
        for a in allUser:
            if a['sid'] == 0:
                sides['left'] += 1
            else:
                sides['right'] += 1
        sid = 0
        gid = sides['left']
        if sides['left'] > sides['right']:
            sid = 1
            gid = sides['right']+10
        db.map.insert({'uid': uid, 'mid':war['mid'], 'sid': sid, 'gid': gid, 'soldiers':[0, 0, 0], 'readTime': 0, 'finish':0})
        db.castal.insert({'mid':war['mid'], 'uid':uid, 'gid':gid, 'soldiers':[0, 0, 0], 'protectTime':-1})#24 hours
        return itsMap(uid)

    @expose('json')
    def addSoldier(self, uid, mid, gid, soldiers):
        uid = int(uid)
        mid = int(mid)
        gid = int(gid)
        soldiers = json.loads(soldiers)
        mainUser = getUser(uid)
        if mainUser.infantrypower < soldiers[0] or mainUser.cavalrypower < soldiers[1] or mainUser.catapult < soldiers[2]:
            return dict(id=0, status = 0, reason="soldiers not enough")


        user = db.map.find_one({'mid':mid, 'uid':uid})
        if gid != user['gid']:
            return dict(id=0, status = 1, reason="not your main city")

        castal = db.castal.find_one({'mid':mid, 'gid':gid, 'uid':uid})
        if castal == None:#client only allow when occupy by my side
            db.castal.insert({'mid':mid, 'uid':uid, 'gid':gid, 'soldiers':soldiers, 'protectTime':-1})
            castal = db.castal.find_one({'mid':mid, 'gid':gid, 'uid':uid})

        mainUser.infantrypower -= soldiers[0]
        mainUser.cavalrypower -= soldiers[1]
        mainUser.catapult -= soldiers[2]

        castal['soldiers'][0] += soldiers[0]
        castal['soldiers'][1] += soldiers[1]
        castal['soldiers'][2] += soldiers[2]
        db.castal.save(castal)
        return dict(id=1)
                    
        
    #cancel immediately
    @expose('json')
    def withdrawSoldier(self, uid, mid, fgid, tgid):
        mid = int(mid)
        uid = int(uid)
        fgid = int(fgid)
        tgid = int(tgid)
        battle = db.battle.find_one({'mid':mid, 'uid':uid, 'fgid':fgid, 'tgid':tgid})
        cur = getNow()
        if battle:
            user = getUser(uid)
            user.infantrypower += battle['soldiers'][0]
            user.cavalrypower += battle['soldiers'][1]
            user.catapult += battle['soldiers'][2]
            db.battle.remove(battle)
            return dict(id=1)
        return dict(id=0, reason='no such battle')
            
        
    @expose('json')
    def accSoldier(self, uid, mid, fgid, tgid):
        mid = int(mid)
        uid = int(uid)
        fgid = int(fgid)
        tgid = int(tgid)
        battle = db.battle.find_one({'mid':mid, 'uid':uid, 'fgid':fgid, 'tgid':tgid})
        cur = getNow()
        user = getUser(uid)
        if battle != None:
            need = cur - battle['timeLeft']
            need = max(battle['timeNeed']-need, 0)
            costCae = math.ceil(need/3600)*2
            if user.cae >= costCae:
                user.cae -= costCae
                battle['timeNeed'] = -1
                db.battle.save(battle)
                #calBattle({'mid':mid})    
                return dict(id=1)
        return dict(id=0)

    @expose('json')
    def groupAttack(self, uid, mid, fgid, tgid, soldiers, timeNeed):
        uid = int(uid)
        mid = int(mid)
        fgid = int(fgid)
        tgid = int(tgid)
        soldiers = json.loads(soldiers)
        timeNeed = int(timeNeed)

        cur = getNow()
        war = db.war.find_one({'mid':mid})
        if war['startTime'] == -1:
            return dict(id=0, status=4, reason='war not begin')
        fc = db.castal.find_one({'mid':mid, 'gid':fgid, 'uid':uid})
        if fc == None:
            return dict(id=0, status =1, reason='no soldiers')
        tcity = db.castal.find_one({'mid':mid, 'gid':tgid})
        if tcity['protectTime'] > cur:
            return dict(id=0, state=3, reason='in protect')
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
        
        exist = db.battle.find_one({'mid':mid, 'fgid':fgid, 'tgid':tgid, 'uid':uid})
        if exist:
            return dict(id=0, statue = 2, reason = 'exist battle')
        battle = {'mid':mid , 'uid':uid,  'fgid':fgid, 'tgid':tgid, 'soldiers':soldiers, 'timeLeft':cur, 'timeNeed':timeNeed}
        db.battle.insert(battle)
        db.castal.save(fc)
        return dict(id=1)
    global helpFriend
    def helpFriend(b):
        cur = getNow()
        castal = db.castal.find_one({'mid':b['mid'], 'gid':b['tgid'], 'uid':b['uid']})
        if castal == None:
            db.castal.insert({'mid':b['mid'], 'uid':b['uid'], 'gid':b['tgid'], 'soldiers':[0, 0, 0], 'protectTime':-1})
            castal = db.castal.find_one({'mid':b['mid'], 'gid':b['tgid'], 'uid':b['uid']})
        castal['soldiers'][0] += b['soldiers'][0]
        castal['soldiers'][1] += b['soldiers'][1]
        castal['soldiers'][2] += b['soldiers'][2]
        db.castal.save(castal)
        #if uid == defid   then it's support 
        db.battleresult.insert({'mid':b['mid'], 'uid':b['uid'], 'defid':b['uid'], 'fgid':b['fgid'], 'tgid':b['tgid'], 'soldiers':b['soldiers'], 'calTime':cur, 'defSoldier':[0, 0, 0],  'attRate':0, 'defRate':0, 'won': 1} )
        
        
    global calBattle
    def calBattle(mid):
        print "calBattle", mid
        cur = getNow()
        battles = db.battle.find({'mid':mid})
        battles = list(battles)

        battles.sort(cmp=lambda x, y: (x['timeLeft']+x['timeNeed'])-(y['timeLeft']+y['timeNeed']))

        for b in battles:
            passTime = cur - b['timeLeft']
            print passTime, b['timeNeed']
            if passTime >= b['timeNeed']:
                db.battle.remove(b)
                user = db.map.find_one({'uid':b['uid']})
                attUser = db.map.find_one({'uid':b['uid']})
                defCastal = db.castal.find({'mid':b['mid'], 'gid':b['tgid']})
                defCastal = list(defCastal)
                #lost less 10% cityNum occupy by who? nearBy will show ti
                attPow = sum(b['soldiers'])
                defPow = 0
                friend = 0
                if len(defCastal) == 0:
                    friend = 1
                for d in defCastal:
                    dUser = db.map.find_one({'uid':d['uid'], 'mid':b['mid']})
                    if dUser['sid'] == attUser['sid']:
                        friend = 1
                        break
                    defPow += sum(d['soldiers'])
                if friend == 1:
                    helpFriend(b)
                    continue
                print "attPow", "defPow", attPow, defPow
                if attPow > defPow:
                    lost = min(attPow/10, defPow/10)
                    attLost = lost
                    defLost = min(lost+defPow/20, defPow)
                else:
                    lost = min(attPow/10, defPow/10)
                    attLost = min(lost+attPow/20, attPow)
                    defLost = lost
                #not zero
                attRate = attLost*100/attPow
                #not zero
                if defPow > 0:
                    defRate = defLost*100/defPow
                else:
                    defRate = 100
                print "attRate", "defRate", attRate, defRate

                attKeep = list(b['soldiers'])
                b['soldiers'][0] = b['soldiers'][0]*(100-attRate)/100
                b['soldiers'][1] = b['soldiers'][1]*(100-attRate)/100
                b['soldiers'][2] = b['soldiers'][2]*(100-attRate)/100

                failUsers = []
                if attPow > defPow:
                    won = 1
                else:
                    won = 0
                if attPow > defPow:
                    db.castal.insert({'mid':b['mid'], 'gid':b['tgid'], 'uid':b['uid'], 'soldiers':b['soldiers'], 'protectTime':-1 })
                else:
                    attUser['soldiers'][0] += b['soldiers'][0]
                    attUser['soldiers'][1] += b['soldiers'][1]
                    attUser['soldiers'][2] += b['soldiers'][2]
                    failUsers.append(attUser)
                    db.map.save(attUser)
                
                for d in defCastal:
                    defKeep = list(d['soldiers'])
                    if won:
                        db.castal.remove(d)
                    d['soldiers'][0] = d['soldiers'][0]*(100-defRate)/100
                    d['soldiers'][1] = d['soldiers'][1]*(100-defRate)/100
                    d['soldiers'][2] = d['soldiers'][2]*(100-defRate)/100
                    db.battleresult.insert({'mid':b['mid'], 'uid':b['uid'], 'defid':d['uid'], 'fgid':b['fgid'], 'tgid':b['tgid'], 'soldiers':attKeep, 'calTime':cur, 'defSoldier':defKeep, 'attRate': attRate, 'defRate': defRate, 'won': won} )
                    if won:
                        defUser = db.map.find_one({'uid':d['uid']})
                        print "defFail", defUser['uid'], d['_id']
                        defUser['soldiers'][0] += d['soldiers'][0]
                        defUser['soldiers'][1] += d['soldiers'][1]
                        defUser['soldiers'][1] += d['soldiers'][1]
                        db.map.save(defUser)
                        failUsers.append(defUser)
                    else:
                        db.castal.save(d)
                for f in failUsers:
                    u = getUser(f['uid'])
                    u.infantrypower += f['soldiers'][0]
                    u.cavalrypower += f['soldiers'][1]
                    u.catapult += f['soldiers'][2]
                    f['soldiers'] = [0, 0, 0]
                    db.map.save(f)
    global wonInMap
    def wonInMap(mid):
        war = db.war.find_one({'mid':mid})
        if war['finish'] == 0 and war['startTime'] != -1:
            castal = db.castal.find({'mid':war['mid']})
            castal = list(castal)
            left = 0
            right = 0
            gids = set()
            cur = getNow()
            for c in castal:
                if c['gid'] not in gids:
                    gids.union([c['gid']])
                    u = db.map.find_one({'uid':c['uid']})
                    if u['sid'] == 0:
                        left += 1
                    else:
                        right += 1

            if left == 0 or right == 0 or (cur-war['startTime']) >= 100*3600:
                for c in castal:
                    cUser = db.map.find_one({'uid':c['uid']})
                    cUser['soldiers'][0] += c['soldiers'][0]
                    cUser['soldiers'][1] += c['soldiers'][1]
                    cUser['soldiers'][2] += c['soldiers'][2]
                    db.map.save(cUser)
                    db.castal.remove(c)
                war['finish'] = 1
                war['left'] = left
                war['right'] = right
                db.war.save(war)

    @expose('json')
    def fetchWarResult(self, uid):
        uid = int(uid)
        user = db.map.find_one({'uid':uid})
        wonInMap(user['mid'])
        war = db.war.find_one({'mid':user['mid']})
        if war['finish'] == 1:
            battle = db.battle.find({'mid':user['mid']})
            for b in battle:
                user = db.map.find_one({'uid':b['uid']})
                user['soldiers'][0] += b['soldiers'][0]
                user['soldiers'][1] += b['soldiers'][1]
                user['soldiers'][2] += b['soldiers'][2]
                db.battle.remove(b)
                db.map.save(user)

            mUser = db.map.find_one({'uid':uid})
            db.map.remove(mUser)
            op = getUser(uid)
            op.infantrypower += mUser['soldiers'][0]
            op.cavalrypower += mUser['soldiers'][1]
            op.catapult += mUser['soldiers'][2]

            left = war['left']
            right = war['right']
            won = 0
            if left > right:
                won = 1
            elif right > left:
                won = 2
            if won == 0:
                return dict(id=1, won=0, cae = 0, stone = 0, left=left, right=right, soldiers = mUser['soldiers'])
            if (won-1) == mUser['sid']:
                op.cae += 3
                changeGoods(uid, 0, 10)
                return dict(id=1, won=1, cae = 3, stone = 10, left=left, right=right, soldiers=mUser['soldiers'])
            else:
                return dict(id=1, won=0,  cae = 0, stone = 0, left=left, right=right, soldiers = mUser['soldiers'])
            return dict(id=1, status = 0, reason="read yet")
        return dict(id=1, status = 1, reason='not finish yet')            
                        




    @expose('json')
    def fetchBattleResult(self, uid):
        cur = getNow()
        uid = int(uid)
        user = db.map.find_one({'uid':uid})
        calBattle(user['mid'])

        results = db.battleresult.find({'uid':uid, 'calTime': {'$gt': user['readTime']}})
        attRes = []
        lastTime = -1
        fgid = -1
        tgid = -1
        defSoldier = 0
        attPow = 0
        attRate = 0
        defRate = 0
        won = 0
        for i in results:
            if i['calTime'] != lastTime or i['fgid'] != fgid or i['tgid'] != tgid:
                if lastTime != -1:
                    attRes.append([fgid, tgid, int(attPow),  int(defSoldier), attRate, defRate, won])
                lastTime = i['calTime']
                attPow = sum(i['soldiers'])
                fgid = i['fgid']
                tgid = i['tgid']
                defSoldier = sum(i['defSoldier'])
                attRate = i['attRate']
                defRate = i['defRate']
                won = i['won']
            else:
                defSoldier += sum(i['defSoldier']) 
        if lastTime != -1:
            attRes.append([fgid, tgid, int(attPow), int(defSoldier), attRate, defRate, won])
        defRes = []
        result = db.battleresult.find({'defid':uid, 'calTime':{'$gt':user['readTime']}})

        for i in result:
            if i['uid'] == uid:
                continue
            attPow = sum(i['soldiers'])
            defPow = sum(i['defSoldier'])
            defRes.append([i['uid'], i['fgid'], i['tgid'], int(attPow), int(defPow), i['attRate'], i['defRate'], i['won']])
        user['readTime'] = cur
        db.map.save(user)
        return dict(id=1, attRes = attRes, defRes = defRes)
            
                
                

        

        


                    

                    
                



                
