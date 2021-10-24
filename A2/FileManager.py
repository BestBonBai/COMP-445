'''
COMP 445 lab assignment 2

@ authors: Hualin Bai (40053833), Qichen Liu (40055916)
@ date: 2021-10-23
@ version: 1.0.0
'''
import os

class FileOperation:
    '''
    The class is to store different operations of File Manager.
    '''
    GetFileList = 1

class FileManager:
    '''
    The class is to manager files in the data directory.
    '''
    def __init__(self):
        # init status is 404 
        self.status = 404
        self.content = ''

    def get_files_list_in_dir(self, dir_path):
        '''
        The method is to get files list in the data directory.
        :param: dir_path
        :return: files list
        '''
        lst_files = []

        for root, dirs, files in os.walk(dir_path):
            # for file in files:
            #     temp = root + '/' + file
            #     lst_files.append(temp[(len(dir_path) + 1):])
            lst_files.append(files)
            # ignore __pycache__ dir
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')

        return lst_files