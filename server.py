#!/bin/python
import select
import signal
import os
import socket
import sys


host = '127.0.0.1'

userInfo = {}
channels = {}
loggedInUser = []
loggedInClient = []
socket_user = {}
channel_user = {}
joinnedChannel = {}

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
    server.setblocking(False)

    while True:
        readable,writeable,exceptional=select.select(inputs, outputs, inputs, 3)
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

    if request.startswith('CREATE'):
        create_channel(socket, request)

    if request.startswith('JOIN'):
        join_channel(socket, request)

    if request.startswith('SAY'):
        say(socket, request)

    if request.startswith('CHANNELS'):
        all_channels(socket, request)


def log_in(socket, request):
    sep_req = request.strip().split(" ")
    if len(sep_req) < 3:
        socket.sendall("RESULT LOGIN 0\n".encode('utf-8'))
        return False
    try:
        userName = sep_req[1]
        passwd = sep_req[2]
        if userName in userInfo:
            if userName in loggedInUser:
                socket.sendall("RESULT LOGIN 0\n".encode('utf-8'))
                return False
            if socket in loggedInClient:
                socket.sendall("RESULT LOGIN 0\n".encode('utf-8'))
                return False
            if passwd == userInfo[userName]:
                socket.sendall("RESULT LOGIN 1\n".encode('utf-8'))
                loggedInUser.append(userName)
                loggedInClient.append(socket)
                socket_user[socket] = userName
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
        socket.sendall("RESULT REGISTER 0\n".encode('utf-8'))
        return False

    try:
        userName = sep_req[1]
        passwd = sep_req[2]
        if userName in userInfo:
            socket.sendall("RESULT REGISTER 0\n".encode('utf-8'))
            return False
        userInfo[userName] = passwd
        socket.sendall("RESULT REGISTER 1\n".encode('utf-8'))
        return True
    except:
        socket.sendall("RESULT REGISTER 0\n".encode('utf-8'))
        return False

def create_channel(socket, request):
    sep_req = request.strip().split(" ")
    channel_name = sep_req[1]

    if socket not in socket_user.keys():
        feedback = "RESULT CREATE " + channel_name + " 0\n"
        socket.sendall(feedback.encode('utf-8'))
        return False
    if channel_name in channels:
        feedback = "RESULT CREATE " + channel_name + " 0\n"
        socket.sendall(feedback.encode('utf-8'))
        return False
    channels[channel_name] = None
    feedback = "RESULT CREATE " + channel_name + " 1\n"
    socket.sendall(feedback.encode('utf-8'))
    return True

def join_channel(socket, request):
    sep_request = request.strip().split(" ")
    channel_name = sep_request[1]
    if channel_name not in channels:
        feedback = "RESULT JOIN " + channel_name + " 0\n"
        socket.sendall(feedback.encode('utf-8'))
        return False

    if socket in joinnedChannel:
        joinnedChannels = joinnedChannel[socket]
        if channel_name in joinnedChannels:
            feedback = "RESULT JOIN " + channel_name + " 0\n"
            socket.sendall(feedback.encode('utf-8'))
            return False
    if not channel_name in channel_user:
        channel_user[channel_name] = [socket]
    else:
        channel_user[channel_name].append(socket)

    if socket in joinnedChannel:
        if not channel_name in joinnedChannel[socket]:
            joinnedChannel[socket].append(channel_name)
    else:
        joinnedChannel[socket] = [channel_name]

    feedback = "RESULT JOIN " + channel_name + " 1\n"
    socket.sendall(feedback.encode('utf-8'))
    return True

def say(socket, request):
    sep_req = request.strip().split(" ")
    channel_name = sep_req[1]
    message = ""
    i = 2
    while i < len(sep_req):
        if i != len(sep_req) - 1:
            message = message + sep_req[i] + " "
        else:
            message = message + sep_req[i]
        i += 1
    userName = socket_user[socket]

    channels[channel_name] = {userName: message}
    feedback = "RECV " + userName + " " + channel_name + " " + message + "\n"
    socket.sendall(feedback.encode('utf-8'))

def all_channels(socket, request):
    sorted_channel = sorted(channels)
    feedback = "RESULT CHANNELS "
    i = 0
    while i < len(sorted_channel):
        if i != len(sorted_channel) - 1:
            feedback += sorted_channel[i] + ", "
        else:
            feedback += sorted_channel[i]
        i += 1
    feedback += "\n"
    socket.sendall(feedback.encode('utf-8'))
if __name__ == '__main__':
    run()


