#-*- coding:utf-8 -*-

import datetime
from os import listdir as LsDir

class Log:
    def __init__(self, filename, path):
        if filename+'.txt' not in LsDir(path):
            file = open(path+'/'+filename+'.txt', 'w')
            file.close()
        self.filename = filename+'.txt'
        self.path = path

    def error(self, message):
        file = open(self.path+'/'+self.filename, 'a')
        file.write("!!!ERROR:"+message+'\n')
        file.close()

    def write(self, message):
        file = open(self.path+'/'+self.filename, 'a')
        file.write(str(datetime.datetime.now())+ " >>> " + message + '\n')
        file.close()
