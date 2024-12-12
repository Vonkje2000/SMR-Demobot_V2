import socket

HOST = "192.168.0.3"  # The server's hostname or IP address
PORT = 42069  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	data = s.recv(1024)
	print(f" {data!r}")
	s.sendall(b"SPEED 100 ALWAYS")
	data = s.recv(1024)
	print(f"Received {data!r}")
	s.sendall(b"HOME")
	data = s.recv(1024)
	print(f" {data!r}")
	s.sendall(b"JMOVE (4, -15, -125, 9, 22, 170)")
	data = s.recv(1024)
	print(f" {data!r}")
	s.sendall(b"SPEED 10 ALWAYS")
	data = s.recv(1024)
	print(f" {data!r}")
	s.sendall(b"JMOVE TRANS (20, 370, 150, 90, 90, 90)")
	data = s.recv(1024)
	print(f" {data!r}")
	s.sendall(b"LMOVE TRANS (20, 470, 150, 90, 90, 90)")
	data = s.recv(1024)
	print(f" {data!r}")
	s.sendall(b"SPEED 100 ALWAYS")
	data = s.recv(1024)
	print(f" {data!r}")
	s.sendall(b"LMOVE TRANS (20, 370, 150, 90, 90, 90)")
	#kawasaki_1.init
	#kawasaki_1.speed(50)
	#kawasaki_1.jmove(1,2,3,4,5,6)
s.close()

#print(f"Received {data!r}")
