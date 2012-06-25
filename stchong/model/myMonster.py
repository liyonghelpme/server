from sqlalchemy import Table, Column
class MyMonster(object):
    def __init__(self, uid, monsters, lastTime):
        self.uid = uid
        self.monsters = monsters
        self.lastTime = lastTime
