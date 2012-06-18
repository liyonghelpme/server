from sqlalchemy import Table, Column
class Monster(object):
    def __init__(self, mid, power, attacker, dragonNum):#[[uid, pow], [uid, pow]]
        self.mid = mid
        self.power = power
        self.attacker = attacker
        self.dragonNum = dragonNum

