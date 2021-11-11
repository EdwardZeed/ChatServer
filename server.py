#!/bin/python
import select
import signal
import os
import socket
import sys


host = '127.0.0.1'

userInfo = {}
result = {}

#Use this variable for your loop
daemon_quit = False

#Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True



def run():
    #Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    # Call your own functions from within 
    # the run() funcion
    port = sys.argv[1]
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((host, port))
    except:
        print("error! cannot connect to server")
    server.listen()

    inputs = [server,]
    outputs = []
    result = {}
    server.setblocking(True)

    while True:
        readable,writeable,exceptional=select.select(inputs, outputs, inputs, 1)
        for socket in readable:
            if socket == server:
                client,addr = socket.accept()

                if not client in inputs:
                    inputs.append(client)
                    request = socket.recv(1024).decode('utf-8')
                    if request:
                        handle_request(request)
                if not client in outputs:
                    outputs.append(client)

            else:
                if not socket in outputs:
                    outputs.append(socket)
                request = socket.recv(1024)
                request = request.decode('utf-8')
                if request:
                    handle_request(request)

        for socket in writeable:
            msg = result[socket]
            msg = msg.encode('utf-8')
            socket.send(msg)





    server.close()

def handle_request(request):
    if request.startswith('LOGIN'):
        log_in(request)

def log_in(socket, request):
    sep_req = request.strip().split(" ")
    if len(sep_req) < 3:
        result[socket] = "RESULT LOGIN 0"
        return False
    userName = sep_req[1]
    passwd = sep_req[2]
    if not userInfo[userName]:
        result[socket] = "RESULT LOGIN 0"
        return False
    else:
        result[socket] = "RESULT LOGIN 1"
        return True



if __name__ == '__main__':
    run()


