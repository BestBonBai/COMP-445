'''
COMP 445 lab assignment 2

@ authors: Hualin Bai (40053833), Qichen Liu (40055916)
@ date: 2021-10-18
@ version: 1.0.0
'''

import sys
import cmd
import argparse
import re
import socket
import threading

class Httpfs(cmd.Cmd):
    """ 
    The Httpfs class is to implement a simple file server.
    """ 

    title = '''

    █████   █████  █████     █████                 ██████         
   ░░███   ░░███  ░░███     ░░███                 ███░░███        
    ░███    ░███  ███████   ███████   ████████   ░███ ░░░   █████ 
    ░███████████ ░░░███░   ░░░███░   ░░███░░███ ███████    ███░░  
    ░███░░░░░███   ░███      ░███     ░███ ░███░░░███░    ░░█████ 
    ░███    ░███   ░███ ███  ░███ ███ ░███ ░███  ░███      ░░░░███
    █████   █████  ░░█████   ░░█████  ░███████   █████     ██████ 
    ░░░░░   ░░░░░    ░░░░░     ░░░░░  ░███░░░   ░░░░░     ░░░░░░  
                                      ░███                        
                                      █████                       
                                      ░░░░░                        

    Welcome to httpfs, Type help or ? to list commands.
    Press 'Ctrl+C' or Type 'quit' to terminate.
    '''
    intro = "\033[1;32;40m{}\033[0m".format(title)
    prompt = 'httpfs '

    # basic httpfs help menu
    def do_help(self, arg):
        '''
        httpfs is a simple file server.

        usage: httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
            -v  Prints debugging messages.
            -p  Specifies the port number that the server will listen and serve at.
                Default is 8080.
            -d  Specifies the directory that the server will use to read/write
                requested files. Default is the current directory when launching the
                application.
        '''
        if not arg or arg == 'help':
            print('''
httpfs is a simple file server.

usage: httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
    -v  Prints debugging messages.
    -p  Specifies the port number that the server will listen and serve at.
        Default is 8080.
    -d  Specifies the directory that the server will use to read/write
        requested files. Default is the current directory when launching the
        application. 
            
            ''')
    
    def do_clear(self, arg):
        '''
        The method is to clear the screen.
        '''
        print('\033c')

    def do_quit(self, arg):
        '''
        The method is to quit the app.
        '''
        print('Thanks for using! Bye!')
        sys.exit(0)

    def emptyline(self):
        '''
        The override method is to use default arguments that -v: False, -p PORT: 8080 and -d PATH-TO-DIR: current dir,
        while typing emptyline.
        '''
        # parse the command from console
        parser_server = argparse.ArgumentParser(description='httpfs is a simple file server'
        , conflict_handler = 'resolve') # conflict_handle is to solve the conflict issue of help argument.
        parser_server.prog = 'httpfs'
        parser_server.usage = parser_server.prog + ' [-v] [-p PORT] [-d PATH-TO-DIR]'
        # add optional argument
        parser_server.add_argument('-v','--verbose',help='Prints debugging messages', action='store_true' )
        parser_server.add_argument('-p','--port',help='Specifies the port number that the server will listen and serve at.\n \
                                    Default is 8080.', type=int, default=8080 )
        parser_server.add_argument('-d','--dir',help='Specifies the directory that the server will use to read/write \
                                    requested files.', default='/' )
        # check if the format of Https is correct
        try:
            # assign args
            args = parser_server.parse_args()
            print(f'[Debug] verbose is : {args.verbose}, port is : {args.port}, path-to-dir is : {args.dir}')
            # run http file server
            self._run_server('localhost',args.port)
        except:
            print('[HELP] Please Enter help to check correct usgae!')  
            return
        

    def default(self, cmd):
        '''
        The method is to Override default fuction to check if the format of Httpfs is correct. 
        :param: cmd : command from console
        '''
        # parse the command from console
        parser_server = argparse.ArgumentParser(description='httpfs is a simple file server'
        , conflict_handler = 'resolve') # conflict_handle is to solve the conflict issue of help argument.
        parser_server.prog = 'httpfs'
        parser_server.usage = parser_server.prog + ' [-v] [-p PORT] [-d PATH-TO-DIR]'
        # add optional argument
        parser_server.add_argument('-v','--verbose',help='Prints debugging messages', action='store_true' )
        parser_server.add_argument('-p','--port',help='Specifies the port number that the server will listen and serve at.\n \
                                    Default is 8080.', type=int, default=8080 )
        parser_server.add_argument('-d','--dir',help='Specifies the directory that the server will use to read/write \
                                    requested files.', default='/' )
        print("[Debug] cmd.split() is : " + str(cmd.split()) )

        # check if the format of Https is correct
        try:
            # assign args
            args = parser_server.parse_args(cmd.split())
            print(f'[Debug] verbose is : {args.verbose}, port is : {args.port}, path-to-dir is : {args.dir}')
            print('\n[News] Running the Http file server ...\n')
            # run http file server
            self._run_server('localhost',args.port)
        except:
            print('[HELP] Please Enter help to get correct format!')  
            return

    def _run_server(self, host, port):
        '''
        The method is to run a simple file server by socket.
        :param: args
        '''
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ip_addr = socket.gethostbyname(host)
            print(f'[Debug] hostname is : {ip_addr}')
            listener.bind((host, port))
            listener.listen(5)
            print('Echo server is listening at', port)
            while True:
                conn, addr = listener.accept()
                threading.Thread(target=self._handle_client, args=(conn, addr)).start()
        finally:
            listener.close()

    def _handle_client(self, conn, addr):
        print(f'\n[Debug] New client from {addr}')
        BUFFER_SIZE = 1024
        try:
            data = b''
            while True:
                part_data = conn.recv(BUFFER_SIZE)
                data += part_data
                if len(part_data) < BUFFER_SIZE:
                    break
            result = data.decode("utf-8")
            print(f'[Debug] Received Request of Client is : \n {result} ')
            # test response
            response = "HTTP1.0/ 200 OK\r\nContext-Type : txt\r\n\r\nServer send response to Client!!!".encode("utf-8")
            print(f'[Debug] Send Response to Client : \n {response}')
            conn.sendall(response)
        finally:
            conn.close()
            print(f'[Debug] Client: {addr} is disconnected from Server.')
                        


# main
if __name__ == '__main__':
    try:
        Httpfs().cmdloop()
    except KeyboardInterrupt:
        print('Thanks for using Httpfs! Bye!')

