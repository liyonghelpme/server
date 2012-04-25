import pymongo
con = pymongo.Connection(host='localhost', port = 27017)
db = con['Rank']
p = db.goods.find()
for i in p:
    try:
        i['goods'] += 1
        db.goods.save(i)
    except:
        pass

