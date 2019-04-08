# import socket
#
# def Main():
#     host = "127.0.0.1"
#     port = 5002
#
#     s = socket.socket()
#     s.connect((host, port))
#
#     filename = input("Filename? ->")
#     print(filename)
#     if filename != "q":
#         s.send(filename.encode())
#         data = s.recv(1024)
#         if data[:6] == "EXISTS":
#             filesize = long(data[6:])
#             message = input("File Exists. Do you want to download?" + str(filesize) + "Bytes")
#             if message == 'Y':
#                 s.send("OK")
#                 f = open(filename, 'wb')
#                 data = s.recv(1024)
#                 totalRecv = len(data)
#                 f.write(data)
#                 while totalRecv < filesize:
#                     data = s.recv(1024)
#                     totalRecv += len(data)
#                     f.write(data)
#                     print("0:,2f".format((totalRecv/float(filesize))*100) + "Done")
#
#                 print("Download complete")
#         else:
#             print("File doesn't exist")
#
#     s.close()
#
# if __name__ == "__main__":
#     Main()
# import socket
# import inotify.adapters
# import sys
#
# host = '127.0.0.1'
# port = 5552
#
# client = socket.socket()
# client.connect((host, port))
#
# i = inotify.adapters.Inotify()
# i.add_watch(sys.argv[1])
#
# message = ' '
#
# for event in i.event_gen(yield_nones=False):
#     (_, type_names, path, filename) = event
#
#     if(type_names[0] == 'IN_MOVED_TO'):
#         message = filename
#         print("File " + filename + " has been moved inside " + path)
#         client.send(message.encode())
#     elif(type_names[0] == 'IN_MOVED_FROM'):
#         message = filename
#         print("File " + filename + " has been moved from " + path)
#         client.send(message.encode())

# import os, time, sys, socket, shutil
#
# host = '127.0.0.1'
# port = 5552
#
# client = socket.socket()
# client.connect((host, port))
#
# path_to_watch = "/home/sebastian/Documents/Scoala/Pexip/ClientFolder"
# before = dict ([(f, None) for f in os.listdir (path_to_watch)])
# while 1:
#   time.sleep (10)
#   after = dict ([(f, None) for f in os.listdir (path_to_watch)])
#   added = [f for f in after if not f in before]
#   removed = [f for f in before if not f in after]
#   message = ' '
#   if added:
#       for i, file in enumerate(added):
#           print("file" + file)
#           path_to_file = os.path.join(path_to_watch, file)
#           print("path_to_file" + path_to_file)
#           f = open(path_to_file, 'rb')
#           l = f.read(1024)
#           print("Added: " + ", ".join(added))
#           message = "Added: " + ", ".join(added)
#           client.send(l)
#           f.close()
#           # client.send(path_to_watch.encode())
#   if removed:
#       print(removed)
#       print("Removed: " + ", ".join(removed))
#       message = "Removed: " + ", ".join(removed)
#       client.send(path_to_watch.encode())
#   before = after

import socket
import threading
import os
import time
import uuid

import buffer

HOST = '127.0.0.1'
PORT = 2345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

path_to_watch = "/home/sebastian/Documents/Scoala/Pexip/ClientFolder"

while 1:
    with s:

        hash_type = input("Enter hash type: ")

        before = dict([(f, None) for f in os.listdir(path_to_watch)])
        time.sleep(10)
        after = dict([(f, None) for f in os.listdir(path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            for i, file in enumerate(added):
                time.sleep(1)
                print(file)
                path_to_file = os.path.join(path_to_watch, file)

                s.send(path_to_file.encode())

                file_size = os.path.getsize(path_to_file)
                file_size = bin(file_size)
                print(file_size)
                s.send(file_size.encode())

                f = open(path_to_file, 'rb')
                l = f.read()
                while(l):
                    s.send(l)
                    l = f.read()
                f.close()
                print("File Sent")


# with s:
#     sbuf = buffer.Buffer(s)
#
#     hash_type = input('Enter hash type: ')
#
#     files = input('Enter file(s) to send: ')
#     files_to_send = files.split()
#
#     for file_name in files_to_send:
#         print(file_name)
#         sbuf.put_utf8(hash_type)
#         sbuf.put_utf8(file_name)
#
#         file_size = os.path.getsize(file_name)
#         sbuf.put_utf8(str(file_size))
#
#         with open(file_name, 'rb') as f:
#             sbuf.put_bytes(f.read())
#         print('File Sent')
