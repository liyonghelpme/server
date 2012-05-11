from sqlalchemy import Table, Column
class Ship(object):
    def __init__(self, uid, sid, state, startTime, timeNeed, goodsKind, num):
        self.uid = uid
        self.sid = sid
        self.state = state
        self.startTime = startTime
        self.timeNeed = timeNeed
        self.goodsKind = goodsKind
        self.num = num
