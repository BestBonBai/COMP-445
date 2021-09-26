'''
COMP 445 lab assignment 1

@ authors: Hualin Bai (40053833), Qichen Liu (40055916)
@ date: 2021-09-20
@ version: 2.0.0
'''

import sys
import cmd
import argparse
import re
import socket
from urllib.parse import urlparse
from HttpClient import HttpRequest, HttpResponse
import shlex # ignore the space in quotes " x x"

class Httpc(cmd.Cmd):
    """ 
    The HttpcLibrary class is to implement cURL command line with basic functions.
    """ 
    
    title = '''

    +++     +++    +++ +++ +++    +++ +++ +++    +++ +++ +++      +++ +++ +++
    +++ +++ +++    +++ +++ +++    +++ +++ +++    +++     +++     +++ +++ +++
    +++ +++ +++        +++            +++        +++ +++ +++    +++
    +++     +++        +++            +++        +++             +++ +++ +++
    +++     +++        +++            +++        +++              +++ +++ +++

    Welcome to httpc, Type help or ? to list commands.
    Press 'Ctrl+C' or Type 'quit' to terminate.

    '''

    intro = "\033[1;33;40m{}\033[0m".format(title)
    prompt = 'httpc '


    # basic httpc help menu
    def do_help(self, arg):
        '''
        httpc is a curl-like application but supports HTTP protocol only.
            Usage:
                httpc command [arguments]
            The commands are: 
                get    executes a HTTP GET request and prints the response.
                post   executes a HTTP POST request and prints the resonse.
                help   prints this screen.
        '''
        if not arg or arg == 'help':
            print('\nhttpc is a curl-like application but supports HTTP protocol only.\n' +
            'Usage: \n' + '\t httpc command [arguments]\n'
            + 'The commands are: \n' + 
            '\t get    executes a HTTP GET request and prints the response.\n' +
            '\t post   executes a HTTP POST request and prints the resonse.\n' +
            '\t help   prints this screen.\n')
        elif arg == 'get':
            print('\nusage: httpc get [-v] [-h key:value] URL\n' +
            'Get executes a HTTP GET request for a given URL.\n' +
            '\t -v Prints the detail of the response such as protocol, status, and headers.\n' +
            '\t -h key:value Associates headers to HTTP Request with the format \'key:value\'.\n')
        elif arg == 'post':
            print('\nusage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n' +
            'Post executes a HTTP POST request for a given URL with inline data or from file.\n' +
            '\t -v Prints the detail of the response such as protocol, status, and headers.\n' +
            '\t -h key:value Associates headers to HTTP Request with the format \'key:value\'.\n' +
            '\t -d string Associates an inline data to the body HTTP POST request.\n' +
            '\t -f file Associates the content of a file to the body HTTP POST request\n' +
            'Either [-d] or [-f] can be used but not both.\n')
        else:
            print('Please input a valid command!!! Type help or ? to get help!!!')
        # return super().do_help(arg)

    def do_clear(self,arg):
        '''
        The method is to clear the screen.
        '''
        print('\033c')

    def do_quit(self,arg):
        '''
        The method is to quit the app.
        '''
        print('Thanks for using! Bye!')
        sys.exit(0)

    def do_get(self, cmd):
        '''
        The method is to execute a HTTP GET request for a given URL.
        :param: cmd : command from console
        :test: get 'http://httpbin.org/status/418'
        :test: get 'http://httpbin.org/get?course=networking&assignment=1'
        :test: get -v 'http://httpbin.org/get?course=networking&assignment=1'
        :test: get -h key:value 'http://httpbin.org/get?course=networking&assignment=1'
        :test: get -h key1:value1 key2:value2 'http://httpbin.org/get?course=networking&assignment=1'
        '''
        # if not cmd: self.do_help('get')
        
        # parse the command from console
        parser_get = argparse.ArgumentParser(description='Get executes a HTTP GET request for a given URL.'
        , conflict_handler = 'resolve') # conflict_handle is to solve the conflict issue of help argument.
        parser_get.prog = 'httpc get'
        parser_get.usage = parser_get.prog + ' [-v] [-h key:value] URL'
        # add optional argument
        parser_get.add_argument('-v','--verbose',help='Prints the detail of the response such as protocol, status, and headers.', action='store_true' )
        parser_get.add_argument('-h','--header',help='Associates headers to HTTP request with the format \'key:value\' ', nargs='+' )

        # add positional argument URL, fix bug : the no expect argument : URL 
        parser_get.add_argument('url',help='a valid http url',default=cmd.split()[-1],nargs='?' )
        # print(cmd.split()[-1])
        # print(cmd.split()[:-1])
        # print("[Debug] cmd.split() is : " + str(cmd.split()) )

        args = parser_get.parse_args(cmd.split()[:-1])
        # print parser help
        # parser_get.print_help()
        print("[Debug] args are : " + str(args) )
        # print(args.url)

        # Check the URL is valid
        if self._is_valid_url(args.url):
            # recall HttpClient to send Http request
        
            # urlparse 
            url_parsed = URL_PARSE(args.url)
            # get request  
            request = self._get_request(url_parsed,args,'GET')
            # use socket to connect server, get response
            response_content = self._client_socket_connect_server(url_parsed,request)

            # Output depends on diffenrent requirements (-v)
            self._print_details_by_verbose(args.verbose,response_content)

    
    # some private methods
    def _is_valid_url(self, url):
        '''
        The method is to check if the url is valid or not.
        :param: url
        :return: boolean
        '''
        # use eval() to omit the ' ' 
        if re.match(r'^https?:/{2}\w.+$',eval(url)):
            print('[Debug] valid url : ' + url)
            return True
        else: 
            print('[Debug] invalid url')
            return False 

    def _is_valid_header(self, header):
        '''
        The method is to check if the header is valid or not.
        :param: header
        :return: boolean
        '''
        # case considers one more key:value
        if len(header) >= 1:
            # check whether header is valid one by one
            for i in range(len(header)):
                if re.match(r'(.+:.+)',header[i]):
                    print('[Debug] valid header : ' + header[i])
                else: 
                    print('[Debug] invalid header : ' + header[i])
                    return False
        else:
            print('[Debug] no header ')
            return False
        return True

    def _get_request(self, url_parsed, args, request_method):
        '''
        The method is to get request by parsed URL, headers, and request method.
        :param: url_parsed
        :param: args : need args.header, args.data, args.file
        :param: request_method : GET or POST
        :return: request
        '''
        if args.header and self._is_valid_header(args.header):
            # case: one more key:value headers
            headers = ''
            for i in range(len(args.header)):
                headers += args.header[i] + '\r\n'
            if request_method == 'GET':
                request = HttpRequest(url_parsed.hostname, url_parsed.path, url_parsed.query, headers)
            else:
                # POST query means infos of (-d) data or (-f) file
                if args.data:
                    request = HttpRequest(url_parsed.hostname, url_parsed.path, args.data, headers)
                else:
                    # TODO: get the info of files
                    pass
        else:
            if request_method == 'GET':
                request = HttpRequest(url_parsed.hostname, url_parsed.path, url_parsed.query,)  
            else: 
                # POST query means infos of (-d) data or (-f) file
                if args.data:
                    request = HttpRequest(url_parsed.hostname, url_parsed.path, args.data,)
                else:
                    # TODO: get the info of files
                    pass
        # get request
        request = request.get_request(request_method)

        return request

    def _client_socket_connect_server(self, url_parsed, request):
        '''
        The method is to connect server using client socket.
        :param: url_parsed
        :param: request
        :param: args
        :return: response_content
        '''
        # use socket to connect server, socket.SOCK_STREAM is for TCP
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            client_socket.connect(url_parsed.address)
            print('--- Connect success ---')
            
            # get response : data (Type: bytes) that need to be decoded by UTF-8 
            data = b''
            while True:
                # send data
                client_socket.sendall(request.encode("utf-8"))
                # receive data
                # MSG_WAITALL waits for full request or error
                response = client_socket.recv(len(request), socket.MSG_WAITALL)
                if response:
                    data += response
                else: break
                # if len(response) < 1 : break
            # decode data, and then parse content
            response_content = HttpResponse(data)

        finally:      
            client_socket.close()
            return response_content
        
    def _print_details_by_verbose(self,args_verbose, response_content):
        '''
        The method is to show different output depends on verbose.
        :param: args_verbose
        :param: response_content
        :return: None
        '''
        # Output depends on diffenrent requirements (-v)
        if args_verbose:
            print('--- Details ---')
            print(response_content.content)
        # other cases
        else: 
            # only print the content.body
            print(response_content.body)

    def do_post(self,cmd):
        '''
        The method is to executes a HTTP POST request for a given URL with inline data or from file.
        :param: cmd : command from console
        :test: httpc post -h Content-Type:application/json -d '{"Assignment": 1}' http://httpbin.org/post
        '''
        # parse the command from console
        parser_post = argparse.ArgumentParser(description='Post executes a HTTP POST request for a given URL with inline data or from file.'
        , conflict_handler = 'resolve') # conflict_handle is to solve the conflict issue of help argument.
        parser_post.prog = 'httpc post'
        parser_post.usage = parser_post.prog + ' [-v] [-h key:value] [-d inline-data] [-f file] URL'
        parser_post.epilog = 'Either [-d] or [-f] can be used but not both. '
        # add_mutually_exclusive_group
        
        parser_post.add_argument('-v','--verbose',help='Prints the detail of the response such as protocol, status, and headers.', action='store_true' )
        parser_post.add_argument('-h', '--header', help='Associates headers to HTTP request with the format \'key:value\' ', nargs='+')
        parser_post.add_mutually_exclusive_group()
        parser_post.add_argument('-d','--data',help='Associates an inline data to the body HTTP POST request.')
        parser_post.add_argument('-f','--file',help='Associates the content of a file to the body HTTP POST request.')
        # add position argument URL, default is to make sure the last argument is URL, add \' for eval() function
        parser_post.add_argument('url',help='a valid http url',default= "'" + shlex.split(cmd)[-1] + "'" ,nargs='?' )
        
        print('[Debug] args is : ' + str(shlex.split(cmd) ))
        args = parser_post.parse_args(shlex.split(cmd)[:-1])

        print("[Debug] args are : " + str(args) )
        # test
        # parser_post.print_help()
        
        # Check the URL is valid
        if self._is_valid_url(args.url):
            # recall HttpClient to send Http request
        
            # urlparse 
            url_parsed = URL_PARSE(args.url)
            # get request  
            request = self._get_request(url_parsed,args,'POST')
            # use socket to connect server, get response
            response_content = self._client_socket_connect_server(url_parsed,request)

            # Output depends on diffenrent requirements (-v)
            self._print_details_by_verbose(args.verbose,response_content)
        

class URL_PARSE:
    '''
    The class is to parse the url and store the parameters of url_parsed.
    :params: url, scheme, hostname, port, ip_address, resource, address
    '''
    def __init__(self, args_url):
        # urlparse 
        self.url = eval(args_url)
        self.url = urlparse(self.url)
        self._assign_param_url()

    def _assign_param_url(self):
        '''
        The method is to assign parameters of URL.
        '''
        # assign parameters of url
        self.scheme = self.url.scheme
        self.hostname = self.url.hostname
        self.path = self.url.path
        self.query = self.url.query
        # websocket has 2 types : ws and wss, the port is 80 and 443 respectively.
        self.port = self.url.port or (443 if self.scheme == 'wss' else 80)
        self.ip_address = socket.gethostbyname(self.hostname)
        self.resource = self.path
        if self.url.query:
            self.resource += '?' + self.query
        # for socket address
        self.address = (self.ip_address, self.port)


# main
if __name__ == '__main__':
    try:
        Httpc().cmdloop()
    except KeyboardInterrupt:
        print('Thanks for using! Bye!')
