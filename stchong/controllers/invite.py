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
from stchong.model import Invite



        

__all__ = ['InviteController']

class InviteController(BaseController):
    def getInvite(self, uid):
        uid = int(uid)
        try:
            user = DBSession.query(Invite).filter_by(uid = uid).one()
        except:
            user = Invite(uid=uid, code = uid, num = 0)
            DBSession.add(user)
            DBSession.flush()
        return user

        
    @expose('json')
    def writeInviteCode(self, uid, code):
        uid = int(uid)
        try:
            code = int(code)
        except:
            return dict(id=0, reason='not number')
        try:
            user = DBSession.query(Invite).filter_by(code=code).one()
            if user.uid == uid:
                return dict(id=0, reason = 'can\'t write to you')
            if user.num >= 10:
                return dict(id=0, reason='times too much')
            try:
                fl = json.loads(user.friendList)
            except:
                fl = []
            try:
                po = fl.index(uid)
                return dict(id=0, reason = 'write yet')
            except:
                pass
            fl.append(uid)
            user.friendList = json.dumps(fl)
            user.num += 1

        except:
            return dict(id=0, reason = 'no suchcode')
        user = getUser(user.uid)
        user.cae += 10

        return dict(id=1)
    @expose('json')
    def getInviteCode(self, uid):
        uid = int(uid)
        user = self.getInvite(uid)
        return dict(id=1, code=user.code)

