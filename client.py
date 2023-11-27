import cmd
import sys
import socket

def main():
    verifyarguments()
    print(sys.argv)
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    connection = makeconnection(server_ip, server_port)
    ChatClient(connection).cmdloop()

def verifyarguments():
    if len(sys.argv) == 1:
        print('incorrect number of arguments supplied\nusage: python3 client.py <server_port>')
        exit(1)

def makeconnection(serverName, serverPort):
    TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPSocket.settimeout(3)
    try:
        TCPSocket.connect((serverName, serverPort))
        return TCPSocket
    except (socket.timeout, ConnectionRefusedError):
        print('No response to connection. Did you choose the right port?')
        quit(1)

class ChatClient(cmd.Cmd):
    # TODO add some sort of passive listener for incoming messages? that sounds kind of hard to be honest
    __slots__ = 'connection'

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def send_message(self, message):
        self.connection.sendall((message + '\n').encode('utf-8'))

    def do_JOIN(self, arg):
        self.send_message(f'JOIN {arg}')

    def do_LIST(self, arg):
        self.send_message('LIST')

    def do_MESG(self, arg):
        self.send_message(f'MESG {arg}')

    def do_BCST(self, arg):
        self.send_message(f'BCST {arg}')

    def do_QUIT(self, arg):
        """
        Disconnect from the server and quit the program
        """
        self.send_message('QUIT')
        self.connection.close()
        quit(0)

if __name__ == '__main__':
    main()
