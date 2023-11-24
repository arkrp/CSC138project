import cmd

class CommandHandler(cmd.Cmd):
    def do_JOIN(self,arg):
        print('join'+arg)
    def do_LIST(self,arg):
        print('LIST'+arg)
    def do_MESG(self,arg):
        print('MESG'+arg)
    def do_BCST(self,arg):
        print('BCST'+arg)
    def do_QUIT(self,arg):
        print('QUIT'+arg)

if __name__ == '__main__':
    CommandHandler().cmdloop()
