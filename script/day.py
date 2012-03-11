import time
import pymongo

con = pymongo.Connection(host='localhost', port=27017)
db = con['Rank']

collect = db.login

while True:
    v = collect.find_one()
    if v != None:
        v['todayNum'] = 0
        collect.save(v)
    time.sleep(24*3600)
