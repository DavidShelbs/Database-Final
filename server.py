# # server.py

# import socket                   # Import socket module

# port = 60000                    # Reserve a port for your service.
# s = socket.socket()             # Create a socket object
# host = socket.gethostname()     # Get local machine name
# s.bind((host, port))            # Bind to the port
# s.listen(5)                     # Now wait for client connection.

# print('Server listening....')

# while True:
# 		conn, addr = s.accept()     # Establish connection with client.
# 		print('Got connection from %s' % str(addr))

# 		data = conn.recv(1024)
# 		print(data.decode('ascii'))

# 		# filename='Proteus.avi'
# 		filename = 'index.txt'
# 		f = open(filename,'rb')
# 		l = f.read(1024)
# 		while (l):
# 				conn.send(l)
# 				print('Sent %s' % conn.decode('ascii'))
# 				l = f.read(1024)
# 		f.close()

# 		print('Done sending')
# 		conn.send('Thank you for connecting')

# 		conn.close()
# 		input("input")





# server.py

import socket                   # Import socket module
import time

start_time = time.time()
# size = 1000000000
size = 1024

port = 60000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print ('Server listening....')

while True:
	conn, addr = s.accept()     # Establish connection with client.
	print ('Got connection from'), addr
	# data = conn.recv(1024)
	data = conn.recv(size)
	print('Server received', repr(data))

	# filename='index.txt'
	filename = 'Girls.Trip.2017.720p.BluRay.x264-[YTS.AG].mp4'
	f = open(filename,'rb')
	# l = f.read(1024)
	l = f.read(size)
	while (l):
		 conn.send(l)
		 print('Sent ',repr(l))
		 # l = f.read(1024)
		 l = f.read(size)
	f.close()

	print('Done sending')
	# conn.send("Thank you for connecting")
	a="Thank you for connecting"
	conn.send(a.encode('ascii'))
	conn.close()

# print("--- %s seconds ---" % (time.time() - start_time))





