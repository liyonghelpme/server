import pymongo
con = pymongo.Connection(host='localhost', port = 27017)
db = con['Rank']

f = file('userid').readlines()
for l in f:
    l = l.replace('\n', '')
    p = db.goods.find_one({'uid':int(l)})
    print p
    p['goods']['0'] += 100
    db.goods.save(p)
