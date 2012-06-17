from sqlalchemy import Table, Column
class Invite(object):
    def __init__(self, uid, code, num):
        self.uid = uid
        self.code = code
        self.num = num
