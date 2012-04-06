from sqlalchemy import Table,Column

class WarRes(object):
    def __init__(self, uid, battleresult, nbattleresult):
        self.uid = uid
        self.battleresult = battleresult
        self.nbattleresult = nbattleresult
