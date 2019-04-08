# import socket
# import threading
# import os
#
# def getFile(name, sock):
#     filename = sock.recv(1024)
#     print(filename)
#     print(os.path.isfile(filename))
#     if os.path.isfile(filename):
#         sock.send("EXISTS" + str(os.path.getsize(filename.decode())))
#         userResponse = sock.recv(1024)
#         if userResponse[:2] == 'OK':
#             with open(filename, 'rb') as f:
#                 bytesToSend = f.read(1024)
#                 sock.send(bytesToSend)
#                 while bytesToSend != '':
#                     bytesToSend = f.read(1024)
#                     sock.send(bytesToSend)
#
#     else:
#         sock.send("ERR")
#
#     sock.close()
#
# def Main():
#     host = '127.0.0.1'
#     port = 5002
#
#     # Default to TCP
#     s = socket.socket()
#     s.bind((host, port))
#
#     s.listen(5)
#
#     print("Server started.")
#     while True:
#         client, address = s.accept()
#         print("Client connected ip: " + str(address))
#         t = threading.Thread(target=getFile, args=("retrThread", client))
#         t.start()
#
#     s.close()
#
# if __name__ == "__main__":
#     Main()

import socket
import hashlib
import threading
import struct

HOST = '127.0.0.1'
PORT = 2345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)
print("Waiting for a connection.....")

conn, addr = s.accept()
print("Got a connection from ", addr)

while True:

    hash_type = conn.recv(1024)
    print('hash type: ', hash_type)
    if not hash_type:
        break

    file_name = conn.recv(1024)
    print('file name: ', file_name)

    file_size = conn.recv(1024)
    file_size = int(file_size, 2)
    print('file size: ', file_size )

    f = open(file_name, 'wb')
    chunk_size = 4096
    while file_size > 0:
        if file_size < chunk_size:
            chuk_size = file_size
        data = conn.recv(chunk_size)
    f.write(data)

    file_size -= len(data)
    f.close()
    print('File received successfully')
    s.close()

# import socket, shutil
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '127.0.0.1'
# port = 5552
#
# address = (host, port)
# server.bind(address)
# server.listen(5)
# print("Starteg listening on: " + host + " " + str(port))
# client, addr = server.accept()
# print("Connection from " + str(addr[0]) + " " + str(addr[1]))
#
# path_to_copy =  "/home/sebastian/Documents/Scoala/Pexip/ServerFolder"
#
# while True:
#     data = client.recv(1024)
#     f = open(data, 'wb')
#     f.write(data)
#     f.close()
#     print("Received " + data.decode() + " from client")
#     client.send(data)


# import socket
#
#
# def server_program():
#     # get the hostname
#     host = socket.gethostname()
#     port = 5001  # initiate port no above 1024
#
#     server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     server_socket.bind((host, port))  # bind host address and port together
#
#     # configure how many client the server can listen simultaneously
#     server_socket.listen(2)
#     conn, address = server_socket.accept()  # accept new connection
#     print("Connection from: " + str(address))
#     while True:
#         # receive data stream. it won't accept data packet greater than 1024 bytes
#         data = conn.recv(1024).decode()
#         if not data:
#             # if data is not received break
#             break
#         print("from connected user: " + str(data))
#         # data = input(' -> ')
#         # conn.send(data.encode())  # send data to the client
#
#     conn.close()  # close the connection
#
#
# if __name__ == '__main__':
#     server_program()


# import socket
#
# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# PORT = 65431        # Port to listen on (non-privileged ports are > 1023)
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             conn.sendall(data)


# #!/usr/bin/env python3
#
# import selectors
# import socket
# sel = selectors.DefaultSelector()
#
# host = '127.0.0.1'
# port = 65431
#
# lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# lsock.bind((host, port))
# lsock.listen()
# print('listening on', (host, port))
# lsock.setblocking(False)
# sel.register(lsock, selectors.EVENT_READ, data=None)
#
# while True:
#     events = sel.select(timeout=None)
#     for key, mask in events:
#         if key.data is None:
#             accept_wrapper(key.fileobj)
#         else:
#             service_connection(key, mask)
#
# def accept_wrapper(sock):
#     conn, addr = sock.accept()  # Should be ready to read
#     print('accepted connection from', addr)
#     conn.setblocking(False)
#     data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
#     events = selectors.EVENT_READ | selectors.EVENT_WRITE
#     sel.register(conn, events, data=data)
#
# def service_connection(key, mask):
#     sock = key.fileobj
#     data = key.data
#     if mask & selectors.EVENT_READ:
#         recv_data = sock.recv(1024)  # Should be ready to read
#         if recv_data:
#             data.outb += recv_data
#         else:
#             print('closing connection to', data.addr)
#             sel.unregister(sock)
#             sock.close()
#     if mask & selectors.EVENT_WRITE:
#         if data.outb:
#             print('echoing', repr(data.outb), 'to', data.addr)
#             sent = sock.send(data.outb)  # Should be ready to write
#             data.outb = data.outb[sent:]
# import socket
# import sys
# from _thread import *
#
# host = ''
# port = 5555
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# try:
#     s.bind((host, port))
# except socket.error as e:
#     print(str(e))
#
# s.listen(5)
# print('Waiting for a connection.')
#
# def client(conn):
#     conn.send(str.encode('Welcome\n'))
#
#     while True:
#         data = conn.recv(2048)
#         reply = 'Server output: ' + data.decode('utf-8')
#         if not data:
#             break
#         conn.sendall(str.encode(reply))
#
#     conn.close()
#
# while True:
#     conn, addr = s.accept()
#     print('connected to: ' + addr[0] + ':' + str(addr[1]))
#
#     start_new_thread(client, (conn,))
#
# import socket
#
# serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# serv.bind(('127.0.0.1', 5556))
# serv.listen(5)
#
# while True:
#     conn, addr = serv.accept()
#     from_client = ''
#
#     while True:
#         data = conn.recv(2048)
#         if not data:
#             break
#         from_client += data.decode()
#         print(data)
#
#         conn.send('I am Server\n')
#
#     conn.close()
#     print('client disconnected')
