# # client.py

# import socket                   # Import socket module

# s = socket.socket()             # Create a socket object

# host = socket.gethostname()     # Get local machine name
# port = 60000                    # Reserve a port for your service.

# s.connect((host, port))
# a="Hello server"
# s.send(a.encode('ascii'))

# with open('received_video.avi', 'wb') as f:
#     print('file opened')
#     while True:
#         print('receiving data...')
#         data = s.recv(1024)
#         print("data=%s" % data.decode('ascii'))
#         if not data:
#             break

#         #write data to a file
#         f.write(data)

# f.close()
# print('Successfully get the file')
# s.close()
# print('connection closed')
# input("input")



# client.py

import socket                   # Import socket module
# size = 1000000000
size = 1024

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
# host = "10.106.62.170"
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
# s.send("Hello server!")
a="Hello server"
s.send(a.encode('ascii'))

# with open('received_file.txt', 'wb') as f:
with open('received_file.mp4', 'wb') as f:
		print ('file opened')
		while True:
				print('receiving data...')
				# data = s.recv(1024)
				data = s.recv(size)
				print('data=%s', (data))
				if not data:
						break
				# write data to a file
				f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')