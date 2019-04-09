import socket
import os
import sys

# Create a socket object, bind the socket to the host of the local machine
# and assign an avaiable port to it.
s = socket.socket()
host = socket.gethostname()
port = 5007
s.bind((host, port))
s.listen(5)
print("Server started.")
# Accept connection from client
client, address = s.accept()
print("Got connection from" + str(address))
# Path of the folder where files will be uploaded
path_to_copy = sys.argv[1]

while True:
    print("Receiving")
    # Decodes message received from client to see if a file was added or if it was removed.
    message = client.recv(128)
    decodedMessage = message.decode()
    print(decodedMessage)
    if decodedMessage == "added":
        # Get the name of the file from client and create path of where the uploaded file
        # will be created.
        name = client.recv(128)
        print(name.decode())
        file_name = os.path.join(path_to_copy, name.decode())
        # Get the filesize of the file to be uploaded from client
        receivedSize = client.recv(128)
        print("Received size: " + receivedSize.decode())
        filesize = int(receivedSize.decode())
        print("File size: " + str(filesize) + " Bytes")
        # Create the file in the upload folder. If filesize is greater than the bytes received
        # per message, continue to receive message from client until the entire file has been transferred.
        with open(file_name, 'wb') as f:
            print("Uploading file...")
            data = client.recv(1024)
            totalReceived = len(data)
            f.write(data)
            while totalReceived < filesize:
                data = client.recv(1024)
                totalReceived += len(data)
                f.write(data)
                print("{0:0.2f}".format((totalReceived/float(filesize))*100) + "% Done")

        print("File has been uploaded.")
        file_name = None
        filesize = None
        receivedSize = None
    if decodedMessage == "removed":
        # Same as in added, gets the name of the file from client and creates the full path to
        # upload folder.
        name = client.recv(128)
        file_name = os.path.join(path_to_copy, name.decode())
        # Check if file exists in the upload folder
        if os.path.exists(file_name):
            # Using the os library we remove the file from there.
            os.remove(file_name)
            print(name.decode() + " has been removed")
            file_name = None
        else:
            print("Error. File does not exist.")
    s.close()
