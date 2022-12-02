# -*- coding: utf-8 -*-
# @Author: John Portella
# @Date:   2022-12-02 09:23:09
# @Last Modified by:   John Portella
# @Last Modified time: 2022-12-02 12:56:25

import logging
import sys
import os
from datetime import datetime

class LoggerFactory(logging.getLoggerClass()): 

    def __init__(self, name, log_dir=None):
        # initialize logger
        super().__init__(name)
        self.setLevel(logging.DEBUG)
        
        # log formatter
        log_format = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"

        # Create stream handler
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.stdout_handler.setLevel(logging.DEBUG)
        self.stdout_handler.setFormatter(logging.Formatter(log_format))        
        self.enable_console_output()

        # Create file handler
        self.file_handler = None
        if log_dir:
            self.add_file_handler(name, log_dir)

    def generate_log_dir(self, log_dir):        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def has_console_handler(self):
        return len([h for h in self.handlers if type(h) == logging.StreamHandler]) > 0
    
    def has_file_handler(self):
        return len([h for h in self.handlers if isinstance(h, logging.FileHandler)]) > 0

    def enable_console_output(self):
        if self.has_console_handler():
            return
        self.addHandler(self.stdout_handler)
    
    def disable_console_output(self):
        if not self.has_console_handler():
            return
        self.removeHandler(self.stdout_handler)
        
    def enable_file_output(self):
        if self.has_file_handler():
            return
        self.addHandler(self.file_handler)
    
    def disable_file_output(self):
        if not self.has_file_handler():
            return
        self.removeHandler(self.file_handler)
    
    def add_file_handler(self, name, log_dir):
        # Format for file log
        log_format = '%(asctime)s | %(name)s | %(levelname)-8s | %(lineno)04d | %(message)s'
        formatter = logging.Formatter(log_format)
        log_name = '{:%Y-%m-%d}.log'.format(datetime.now())
        log_file = os.path.join(log_dir, log_name)
        # Create log dir
        self.generate_log_dir(log_dir)
        # Create file handler for logging to a file
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(formatter)
        self.addHandler(self.file_handler)

class StaticLoggerFactory:
    _LOG = None

    def __new__(cls, name, log_dir=None):
        if cls._LOG is None:
            # initialize singleton instance
            cls._LOG = super().__new__(cls)

            # initialize logger            
            cls._LOG = logging.getLogger(name)
            cls._LOG.setLevel(logging.DEBUG)

            # log formatter
            log_format = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"

            #Create stream handler
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.DEBUG)
            stdout_handler.setFormatter(logging.Formatter(log_format))                
            cls._LOG.addHandler(stdout_handler)

            if log_dir:                
                
                #log formatter   
                log_format = '%(asctime)s | %(name)s | %(levelname)-8s | %(lineno)04d | %(message)s'
                
                #Logname
                log_name = '{:%Y-%m-%d}.log'.format(datetime.now())
                formatter = logging.Formatter(log_format)
                
                #Create log dir
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                log_file = os.path.join(log_dir, log_name)

                #create file handler
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                cls._LOG.addHandler(file_handler)
                            
        return cls._LOG

def set_logger(name, log_dir=None):
    # initialize logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # log formatter
    log_format = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"

    #Create stream handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(logging.Formatter(log_format))                
    logger.addHandler(stdout_handler)

    if log_dir:
        #log formatter   
        log_format = '%(asctime)s | %(name)s | %(levelname)-8s | %(lineno)04d | %(message)s'
        
        #Logname
        log_name = '{:%Y-%m-%d}.log'.format(datetime.now())
        formatter = logging.Formatter(log_format)
        
        #Create log dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, log_name)

        #create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

if __name__ == '__main__':
    quiet_log = LoggerFactory('custom class', log_dir='logs')
    quiet_log.warning('Test Warning')
    quiet_log.error('Test Error')
    quiet_log.disable_console_output()
    quiet_log.info('Test Info')
    quiet_log.enable_console_output()
    quiet_log.disable_file_output()
    quiet_log.critical('Test Critical')

    logger = set_logger(name="custom def", log_dir='logs')
    logger.warning('Test Warning')
    logger.error('Test Error')
    
    singleton_logger = StaticLoggerFactory(name="singleton log", log_dir='logs')
    singleton_logger.info("Hello, Logger")
    singleton_logger2 = StaticLoggerFactory(name="singleton log", log_dir='logs')
    singleton_logger2.debug("bug occured")
    
    print("Id of logger : {}".format(str(id(singleton_logger))))
    print("Id of logger2 : {}".format(str(id(singleton_logger2))))
    
    