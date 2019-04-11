# server.py

import socket                 

port = 60000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print ('Server listening....')

# doesnt need to be in a loop rn but can keep for later
while True:
	conn, addr = s.accept()     # Establish connection with client.
	print ('Got connection from'), addr
	data = conn.recv(1024)
	print('Server received', repr(data))

	# filename = 'Girls.Trip.2017.720p.BluRay.x264-[YTS.AG].mp4'
	# filename = 'E:Movies\\Action\\Hunger Games\\The.Hunger.Games.Catching.Fire.2013.720p.BluRay.x264.YIFY.mp4'
	print ("Please insert your location")
	print ("Example: E:Movies\\Action\\Hunger Games\\The.Hunger.Games.Catching.Fire.2013.720p.BluRay.x264.YIFY.mp4")
	filename = input()
	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
		 conn.send(l)
		 l = f.read(1024)
	f.close()

	print('Done sending')
	a="Thank you for connecting"
	conn.send(a.encode('ascii'))
	conn.close()
	break


