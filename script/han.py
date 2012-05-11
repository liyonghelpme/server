import pymongo
con = pymongo.Connection(host='localhost', port=27017)
db = con['Rank']

f = open('all').readlines()
for u in f:
    u = u.replace('\n', '')
    user = db.goods.find_one({'uid':int(u)})
    user['goods']['0'] += 5
    db.goods.save(user)
for u in f[4:100]:
    u = u.replace('\n', '')
    user = db.goods.find_one({'uid':int(u)})
    user['goods']['0'] += 5
    db.goods.save(user)


