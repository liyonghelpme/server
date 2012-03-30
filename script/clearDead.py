import pymongo
con = pymongo.Connection(host='localhost', port=27017)
db = con['Rank']
dead = db.deadDay.find_one()
if dead == None:
    dead = {'deadDay':7}
else:
    dead['deadDay'] -= 1

db.deadDay.save(dead)
