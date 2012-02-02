i = 0
ports = [8081, 8082, 8083]
while i < len(ports):
	f = file("development.ini").read()
	f = f.replace("port = 8080", "port = "+str(ports[i]))
	n = file("development"+str(i)+".ini", 'w')
	n.write(f)
	n.close()
	i += 1
