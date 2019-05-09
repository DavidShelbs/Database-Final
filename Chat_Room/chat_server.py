import sqlite3
import socket
import select
from _thread import *
import sys
import time


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain
with any two hosts
The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow
"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP_address = socket.gethostbyname(socket.gethostname())
Port = 5001
server.bind((IP_address, Port))
print("Server Running on " + IP_address + ":" + str(Port))
server.listen(100)
list_of_clients=[]

def clientthread(conn, addr):
    ip = addr[0]
    user_name = '\0'
    time.sleep(.1)

    data_base = sqlite3.connect('tech_support.db')
    cursor = data_base.execute("SELECT IP_Address, User_Name FROM USERS WHERE IP_Address = ?", (ip,))

    for row in cursor:
        user_name = row[1]

    if user_name == '\0':
        while user_name == '\0':
            conn.send(b"Use ![Username] to set username before entering the chatroom.")
            message = conn.recv(2048)
            decMessage = message.decode()
            if decMessage[0] == "!":
                new_user_name = decMessage[1:]
                user_name = new_user_name
                message = user_name + " has joined the channel!"
                data_base.execute("INSERT INTO USERS (IP_Address, User_Name) VALUES (?, ?)", (ip, user_name));
                data_base.commit()
                message = message.encode()
                print(message.decode())
                message_to_send = message.decode()
                broadcast(message_to_send,conn)

    else:
        message = user_name + " has joined the channel!"
        print(message)
        message_to_send = message
        broadcast(message_to_send,conn)

    while True:
        try:
            message = conn.recv(2048)
            if message:
                if message.decode() != '\n':
                    decMessage = message.decode()
                    if decMessage[0] == "!":
                        new_user_name = decMessage[1:]
                        message = user_name + " has changed their name to " + new_user_name
                        user_name = new_user_name
                        data_base.execute("UPDATE USERS set User_Name = ? where IP_Address = ?", (user_name, ip))
                        data_base.commit()
                        message = message.encode()
                        print(message.decode())
                        message_to_send = message.decode()
                        broadcast(message_to_send,conn)
                    else:
                        print("<" + user_name + "> " + message.decode())
                        message_to_send = "<" + user_name + "> " + message.decode()
                        broadcast(message_to_send,conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

"""
Setup Database
"""
db = sqlite3.connect('tech_support.db')
data_base = db.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS USERS
         (IP_Address    INT     PRIMARY KEY     NOT NULL,
         User_Name      TEXT    NOT NULL);''')

while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    start_new_thread(clientthread, (conn,addr))

conn.close()
server.close()
db.close()
