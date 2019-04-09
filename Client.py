import socket
import sys
import os
import time

# Create a socket object, and connects the client to the host and port of the server.
s = socket.socket()
host = socket.gethostname()
port = 5007
s.connect((host, port))

# Path of the folder that is monitorized
path_to_watch = sys.argv[1]
# Dictionary of the files already present in the monitored folder.
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while True:
    # Every 5 seconds it looks through the folder to see if files were added or removed.
    # Added and removed files are both stored in different dictionaries to hold the list of files
    # each time it looks through the folder. The os library has been used to monitor the folder.
    time.sleep(5)
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added:
        for i, file in enumerate(added):
            # Message sent to the server so it knows a file has been added
            message = "added"
            s.send(message.encode())
            print("Added file " + file)
            # Message sent to let the server know the name of the file that was added
            s.send(file.encode(encoding='UTF-8',errors='strict'))
            # Full path of the added file
            path_to_file = os.path.join(path_to_watch, file)
            f = open(path_to_file, 'rb')
            # Filesize sent to the server so it knows whether to continue sending messages
            # to fully upload the file. Encoded in utf-8 as files of bigger size had ASCII characters present.
            filesize = str(os.path.getsize(path_to_file))
            s.send(filesize.encode(encoding='UTF-8',errors='strict'))
            filesize = int(filesize)
            with open(path_to_file, 'rb') as f:
                # Starts sending the file over to the server by continously sending data until
                # the whole file has been uploaded.
                data = f.read(1024)
                totalReceived = len(data)
                s.send(data)
                while totalReceived < filesize:
                    data = f.read(1024)
                    totalReceived += len(data)
                    s.send(data)
            print("Done reading")
            filesize = None
            path_to_file = None
            time.sleep(1)
    if removed:
        # Message sent to the server so it knows a file has been removed.
        # Loops through the removed files and sends a message to the server with the removed file.
        for i, file in enumerate(removed):
            message = "removed"
            s.send(message.encode())
            print("Removed file " + file)
            s.send(file.encode())
            time.sleep(0.5)
    before = after
