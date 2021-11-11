#!/bin/python
import signal
import os
import sys
import socket

host = '127.0.0.1'

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
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(host, port)
    except:
        print("error")


    server.listen(2)
    server.close()

    pass


if __name__ == '__main__':
    run()


