from sqlalchemy import Table, Column
class Mana(object):
    def __init__(self,userid,mana,boundary,lasttime):
            self.userid=userid
            self.mana=mana
            self.boundary=boundary
            self.lasttime=lasttime

