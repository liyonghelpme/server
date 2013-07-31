import time
import os
while True:
	cur = int(time.mktime(time.localtime()))
	os.system('cat buycae.log >> total.log')
	os.system('cp buycae.log cae.log.'+str(cur))
	os.system('mv buycae.log /var/www/html/cae.log')
	os.system('cp total.log /var/www/html')
	os.system('echo > buycae.log')
	time.sleep(25*3600)
