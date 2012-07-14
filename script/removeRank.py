import time
import pymongo

while True:
    con = pymongo.Connection(host='localhost', port=27017)
    db = con['Rank']
    db.rankYet.remove()
    time.sleep(24*3600)
