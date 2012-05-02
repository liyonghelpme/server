import time
import pymongo

con = pymongo.Connection(host='localhost', port=27017)
db = con['Rank']

collect = db.rank

while True:
    res = collect.find().sort('food', pymongo.DESCENDING)
    arr = []
    db.order.remove()
    k = 0
    for r in res:
        arr.append(r)
        collect.update({'uid':r['uid']}, {'$set': {'order':k}})
        k += 1
    db.result.remove()
    db.result.insert({'res':arr})
    
    time.sleep(3600)
