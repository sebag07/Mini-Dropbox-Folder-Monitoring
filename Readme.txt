Python has been used to develop the program and it was built on Linux. The libraries used for the Server and Client were: socket, sys, os, time.

To run the program, frist type python Server.py <directory> in the terminal. The Server.py file takes one directory as argument. It will upload the changes made to the Client directory.

Second, run the Client.py file by typing python Client.py <directory> in the terminal. The Client.py file takes one directory as argument and it keeps monitoring changes in the directory and uploads the changes to the server.

To stop the program, use ctrl+c in the client terminal, then in the server terminal. The way the app was developed was to be a continuous stream of data every few seconds, and asking for input from user could have been counter-intuitive to the flow of the program.
