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
    port = int(sys.argv[1])
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((host, port))
    except:
        print("error! cannot connect to server")
    server.listen()

    inputs = [server]
    outputs = []
    result = {}
    server.setblocking(False)

    while True:
        readable,writeable,exceptional=select.select(inputs, outputs, inputs, 1)
        for s in readable:
            if s == server:
                client,addr = server.accept()
                client.setblocking(False)

                # if not client in inputs:
                #     inputs.append(client)
                #     request = socket.recv(1024).decode('utf-8')
                #     if request:
                #         handle_request(request)
                # if not client in outputs:
                #     outputs.append(client)
                inputs.append(client)

            else:
                # if not socket in outputs:
                #     outputs.append(socket)
                request = s.recv(1024)
                request = request.decode('utf-8')
                if request:
                    handle_request(s, request)
                else:
                    inputs.remove(s)

        # for s in writeable:
        #     msg = result[socket]
        #     msg = msg.encode('utf-8')
        #     socket.send(msg)

        # request = client.recv(1024)
        # print(request)
        # client.sendall(request)





    # server.close()

def handle_request(socket, request):
    if request.startswith('LOGIN'):
        log_in(socket, request)

    if request.startswith('REGISTER'):
        register(socket, request)


def log_in(socket, request):
    sep_req = request.strip().split(" ")
    if len(sep_req) < 3:
        socket.sendall("RESULT LOGIN 0\n".encode('utf-8'))
        return False
    try:
        userName = sep_req[1]
        passwd = sep_req[2]
        if userName in userInfo:
            if passwd == userInfo[userName]:
                socket.sendall("RESULT LOGIN 1\n".encode('utf-8'))
                return True
            else:
                socket.sendall("RESULT LOGIN 0\n".encode('utf-8'))
                return False
        else:
            socket.sendall("RESULT LOGIN 0\n".encode('utf-8'))
            return False
    except:
        socket.sendall("RESULT LOGIN 0\n".encode('utf-8'))
        return False

def register(socket, request):
    sep_req = request.strip().split(" ")
    if len(sep_req) < 3:
        socket.sendall("RESULT RESGITER 0\n".encode('utf-8'))
        return False

    try:
        userName = sep_req[1]
        passwd = sep_req[2]
        if userName in userInfo:
            socket.sendall("RESULT RESGITER 0\n".encode('utf-8'))
            return False
        userInfo[userName] = passwd
        socket.sendall("RESULT RESGITER 1\n".encode('utf-8'))
        return True
    except:
        socket.sendall("RESULT RESGITER 0\n".encode('utf-8'))
        return False




if __name__ == '__main__':
    run()


