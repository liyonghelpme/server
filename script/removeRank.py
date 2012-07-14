import time
import pymongo

con = pymongo.Connection(host='localhost', port=27017)
db = con['Rank']
db.rankYet.remove()
