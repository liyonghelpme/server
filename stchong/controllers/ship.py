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
from stchong.model import Ship, Mana
import json

from stchong.controllers.util import *

__all__ = ['ShipController']


class ShipController(BaseController):
    @expose('json')
    def speedup(self, uid):
        print "shipSpeedup", uid
        uid = int(uid)
        ship = getShip(uid)
        if ship.state != 1:
            return dict(id=0, reason = "not working")
        needTime = ship.timeNeed
        beginTime = ship.startTime
        curTime = getTime()
        curTime -= beginTime
        needTime -= curTime
        needTime = max(0, needTime)
        if needTime == 0:
            return dict(id=1)
        cost = (needTime+3599)/3600+5
        mana = DBSession.query(Mana).filter_by(userid=uid).one()
        if mana.mana >= cost:
            mana.mana -= cost
            ship.timeNeed = 0
            return dict(id=1)
        return dict(id=0)
    global ShipCost
    ShipCost = [130000, 50]
    @expose('json')
    def buyShip(self, uid, kind):
        print "buyShip", uid, kind
        uid = int(uid)
        kind = int(kind)
        ship = getShip(uid)
        user = getUser(uid)
        if ship.state != -1:
            return dict(id=0, reason = "buy ship yet")
        if kind == 0:
            if user.corn >= ShipCost[kind]:
                user.corn -= ShipCost[kind]
                ship.state = 0
                return dict(id=1)
        elif kind == 1:
            if user.cae >= ShipCost[kind]:
                user.cae -= ShipCost[kind]
                ship.state = 0
                return dict(id=1)
        return dict(id=0, reason = "res not enough")
    global TradeKinds
    TradeKinds = [
    [2, 0, 1, 1000, 10*60],
    [2, 0, 10, 11000, 15*60],
    [2, 0, 100, 120000, 30*60],
    [1, 0, 100, 1000, 15*60],
    [1, 0, 1000, 8000, 2*3600],
    [1, 0, 10000, 60000, 8*3600],
    [0, 1, 50000, 2000, 10*60],
    [0, 1, 10000, 1000, 4*3600],
    [0, 1, 5000, 600, 12*3600],
    ]
    @expose('json')
    def trade(self, uid, kind):
        print "trade", uid, kind
        uid = int(uid)
        kind = int(kind)
        trading = TradeKinds[kind]
        cost = trading[0]
        user = getUser(uid)
        ship = getShip(uid)
        if ship.state != 0:
            return dict(id=0, reason="not free")
        coinCost = 0
        foodCost = 0
        caeCost = 0

        if cost == 0:
            coinCost = trading[2]
        elif cost == 1:
            foodCost = trading[2]
        else:
            caeCost = trading[2]
        if user.corn >= coinCost and user.food >= foodCost and user.cae >= caeCost:
            user.corn -= coinCost
            user.food -= foodCost
            user.cae -= caeCost

            ship.startTime = getTime()
            ship.timeNeed = trading[4]
            ship.state = 1
            ship.goodsKind = trading[1]
            ship.num = trading[3]
            return dict(id=1, kind=kind)
        return dict(id=0)

    @expose('json')
    def collect(self, uid): 
        print "collect", uid
        uid = int(uid)
        ship = getShip(uid)
        if ship.state != 1:
            return dict(id=0, reason="not working")
        user = getUser(uid)
        kind = ship.goodsKind
        coinAdd = 0
        foodAdd = 0
        if kind == 0:
            coinAdd = ship.num
        else:
            foodAdd = ship.num
        user.corn += coinAdd
        user.food += foodAdd

        ship.state = 0
        return dict(id=1, coin = coinAdd, food = foodAdd)



            
