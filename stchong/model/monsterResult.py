from sqlalchemy import Table, Column
class MonsterResult(object):
    def __init__(self, uid, mid, dragonNum, power, readYet, totalNum):
        self.uid = uid
        self.mid = mid
        self.dragonNum = dragonNum
        self.power = power
        self.readYet = readYet
        self.totalNum = totalNum

