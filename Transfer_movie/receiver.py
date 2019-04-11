# client

import socket                   
import time

start_time = time.time()

s = socket.socket()             # Create a socket object
# host = socket.gethostname()     # Get local machine name
host = "10.106.62.170"
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
a="Hello server"
s.send(a.encode('ascii'))

# with open('received_file.mp4', 'wb') as f:
print ("Please insert your location and title")
print ("Example: D:received_file.mp4")
name = input()
with open(name, 'wb') as f:
	print ('file opened')
	while True:
		data = s.recv(1024)
		if not data:
			break
		# write data to a file
		f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')
print(((time.time() - start_time)/60), " min.")