#!/usr/bin/env python3

__author__ = 'Adam Marciniak'
__version__ = '0.1.0'
__license__ = 'MIT'

import os.path
import logging
import subprocess
from platform import python_version

class upload2Insta():

    #__username = 'laerm_und_liebe'
    #__password = '3160633'
    __username = 'hansi_petri'
    __password = 'hansi_petri13'
    

    def __init__(self):
        logging.basicConfig(filename='log_upload.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


    def upload(self, imagepath, caption = '#photobox'):

        if self.__checkFile(imagepath) :
            try:
                output = subprocess.check_output(['instapy', '-u %s' %(self.__username), '-p %s' %(self.__password), '-t %s' %(caption), '-f%s' %(imagepath)])

                if not b'Done.' in output:
                    logging.debug('Upload unsuccessfull for file %s: %s' %(imagepath, output))

            except OSError as e:
                if e.errno == os.errno.ENOENT:
                    # handle file not found error.
                    logging.debug('instapy-cli not installed')
                else:      
                     logging.debug('Something went wrong during upload.')

    def __checkFile(self, imagepath):
        if not os.path.isfile(imagepath):
            logging.debug('File does not exist: %s' %(imagepath))
            return False
        
        if not (imagepath.lower().endswith('.jpg') or imagepath.lower().endswith('.jpeg')):
            logging.debug('File is invalid: %s' %(imagepath))
            return False
        
        return True


if __name__ == '__main__':
    u2i = upload2Insta()
    u2i.upload('test.jpg')