#Nicolas Gugliemo
#Garret Learned
#Hannah Nelson
#Fabrice Auriole Yonkeu Ebenye
#Estefany Aguilar Luna
#CSC/CPE 138 Section 01
#11/26/2023
#client program for the TCP chatroom

import cmd
import sys
import os
import socket
import threading

def main():
    verifyarguments()
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    connection = makeconnection(server_ip, server_port)
    connection.settimeout(None)
    #start a threat which prints out everything we recieve!
    mythread = threading.Thread(target= printloop, args= (connection,))
    mythread.start()
    ChatClient(connection).cmdloop()

def printloop(connection):
    while(True):
        response = connection.recv(1024).decode('utf-8')
        print(response)


def verifyarguments():
    if len(sys.argv) == 1:
        print('incorrect number of arguments supplied\nusage: python3 client.py <server_port>')
        os._exit(1)

def makeconnection(serverName, serverPort):
    TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPSocket.settimeout(3)
    try:
        TCPSocket.connect((serverName, serverPort))
        return TCPSocket
    except (socket.timeout, ConnectionRefusedError):
        print('No response to connection. Did you choose the right port?')
        os._exit(1)

class ChatClient(cmd.Cmd):
    # TODO add some sort of passive listener for incoming messages? that sounds kind of hard to be honest
    __slots__ = 'connection'

    def __init__(self, connection):
        super().__init__()
        self.prompt = ""
        self.connection = connection

    def send_message(self, message):
        self.connection.sendall((message + '\n').encode('utf-8'))

    def do_JOIN(self, arg):
        self.send_message(f'JOIN {arg}')

    def do_LIST(self, arg):
        self.send_message('LIST')

    def do_MESG(self, *arg):
        print(f'{arg[0]}')
        self.send_message(f'MESG {arg[0]}')

    def do_BCST(self, arg):
        self.send_message(f'BCST {arg}')

    def do_QUIT(self, arg):
        """
        Disconnect from the server and quit the program
        """
        self.send_message('QUIT')
        print("You have Quit.")
        self.connection.close()
        os._exit(0)

if __name__ == '__main__':
    main()
