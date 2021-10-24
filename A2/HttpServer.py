'''
COMP 445 lab assignment 2

@ authors: Hualin Bai (40053833), Qichen Liu (40055916)
@ date: 2021-10-23
@ version: 1.0.0
'''
import re
from FileManager import FileOperation

class HttpMethod:
    '''
    The class is to store request method name.
    '''
    Get = "GET"
    Post = "POST"
    Invalid = "Invalid"

class HttpRequestParser:
    '''
    The class is to parser the Http Request from Client.
    '''
    def __init__(self, request):
        '''
        The method is to parser the request from Client.
        :param: request
        '''
        # default values
        self.contentType = "application/json"

        # split header and body of request
        self.http_header, self.http_body = request.split('\r\n\r\n')
        # get method, resource, version 
        header_lines = self.http_header.split('\r\n')
        self.method, self.resource, self.version = header_lines[0].split(' ')
        # get contentType
        for index, line in enumerate(header_lines):
            if re.match(r'Content-Type', line):
                self.contentType = line.split(' ')[1]
                break
        # set operation
        self._set_operation()

    def _set_operation(self):
        '''
        The method is to set the file operation by different request.
        '''
        # GET method
        if self.method == HttpMethod.Get:
            if self.resource == '/':
                self.operation = FileOperation.GetFileList

        # POST method

        


        