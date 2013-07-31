import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='2e4n5k2w2x',db='stcHong')
except Exception, e:
    print e
    sys.exit()
