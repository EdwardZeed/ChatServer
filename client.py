import socket
import sys

port = int(sys.argv[1])
host = '127.0.0.1'

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))
while True:
    msg = input()
    if (msg.lower() == "q"):
        break
    socket.send(msg.encode('utf-8'))
    feedback = socket.recv(1024)
    print(feedback.decode('utf-8'))