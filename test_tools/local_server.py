#!/usr/bin/python

import socket

HOST = '127.0.0.1'       
PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

while 1:
#	print 'Connected by', addr
	while 1:
		data = conn.recv(4096)
		if not data: break
		print data

conn.close()
