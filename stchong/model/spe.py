from sqlalchemy import Table, Column
class Spe(object):
    def __init__(self, uid, specialgoods):
        self.uid = uid
        self.specialgoods = specialgoods
