import os
os.system('cat screenlog* | grep debug > res.txt')
os.system('mvlog.sh')
f = file('res.txt').readlines()
for l in f:
	l = l.replace('\n', '')
	l = l.replace('tg2', 'localhost:8000')
	l = l.replace('war', 'localhost:9400')
	os.system('wget '+l + ' -o  debug.'+l)

