#!/usr/bin/python

import socket
from random import randrange


HOST = '127.0.0.1'       
PORT = 5005

ka_string = "99,ka,0,0;"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while 1:
	conn, addr = s.accept()

	while 1:
		print 'Connected by', addr
		data = conn.recv(1024)
		if not data: break
		print data
		if data == ka_string:
			conn.sendall(str(randrange(100)) + ',' + str(randrange(100)) + ',' + str(randrange(100)))

	conn.close()



