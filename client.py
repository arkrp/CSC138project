import cmd, sys, socket

def main():
    verifyarguments()
    print(sys.argv)
    connection = makeconnection('127.0.0.1',int(sys.argv[1]));
    ChatClient(connection).cmdloop()

def verifyarguments():
    if(len(sys.argv) == 1):
        print('incorrect number of arguments supplied\nusage: python3 client.py <server_port>')
        exit(1)

def makeconnection(serverName,serverPort):
    TCPSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    TCPSocket.settimeout(3)
    try:
        TCPSocket.connect((serverName,serverPort))
        return TCPSocket
    except (socket.timeout, ConnectionRefusedError):
        print('No response to connection. Did you choose the right port?')
        quit(1)
    

class ChatClient(cmd.Cmd):
    #TODO add some sort of passive listener for incoming messages? that sounds kind of hard to be honest
    __slots__ = 'connection'
    def __init__(self,connection):
        super().__init__()
        self.connection = connection
    def do_JOIN(self,arg):
        self.connection.sendall(b'JOIN')
        #TODO actual logic for this
    def do_LIST(self,arg):
        self.connection.sendall(b'LIST')
        print('LIST'+arg)
        #TODO actual logic for this
    def do_MESG(self,arg):
        self.connection.sendall(b'MESG')
        print('MESG'+arg)
        #TODO actual logic for this
    def do_BCST(self,arg):
        self.connection.sendall(b'BCST')
        print('BCST'+arg)
        #TODO actual logic for this
    def do_QUIT(self,arg):
        """
        Disconnect from the server and quit the program
        """
        self.connection.sendall(b'QUIT')
        self.connection.close()
        quit(0)

if __name__ == '__main__':
    main()
