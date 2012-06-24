from sqlalchemy import Table, Column
class Monster(object):
    def __init__(self, uid, mid, power, attacker, dragonNum):
        self.uid = uid
        self.power = power
        self.attacker = attacker
        self.dragonNum = dragonNum
