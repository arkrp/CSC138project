import cmd

class ChatClient(cmd.Cmd):
    def do_JOIN(self,arg):
        #TODO
        print('join'+arg)
    def do_LIST(self,arg):
        #TODO
        print('LIST'+arg)
    def do_MESG(self,arg):
        #TODO
        print('MESG'+arg)
    def do_BCST(self,arg):
        #TODO
        print('BCST'+arg)
    def do_QUIT(self,arg):
        #TODO
        """
        disconnect and quit the program
        """
        self.disconnect()
        quit()
    def disconnect(self):
        #TODO
        """
        disconnect from stuff
        """
        pass

if __name__ == '__main__':
    ChatClient().cmdloop()
