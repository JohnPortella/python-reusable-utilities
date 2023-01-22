# -*- coding: utf-8 -*-
# @Author: John Portella
# @Date:   2023-01-22 11:07:33
# @Last Modified by:   John Portella
# @Last Modified time: 2023-01-22 14:37:50
import paramiko, os
from ftplib import FTP

class PyFileTransfer(object):
    """
    A class for performing file transfer using FTP or SFTP.    
    """

    def __init__(self, typeProtocol='ftp', hostname = 'localhost', so='unix', port = None, timeout = None):
        """
        Initializes the PyFileTransfer object and sets the connection parameters.
        Args:
            typeProtocol (str): 'ftp' or 'sftp' protocol to use for the file transfer
            hostname (str): the hostname or IP address of the server
            so (str): 'unix' or 'win' depending on the operating system of the server
            port (int): the port number to use for the connection, if None it will use default port for the protocol
            timeout (int): the timeout for the connection, if None it will use default timeout
        """

        #Protocol
        self.__typeProtocol = typeProtocol
        #host
        self.__hostname = hostname
        #so        
        if so == 'unix':
            self.__SEP = '/'
        elif so == 'win':
            self.__SEP = chr(92)   
        #timeout
        self.__timeout = timeout
        #port
        if port:
            self.__port = port
        #open transfering
        if self.__typeProtocol == 'ftp':
            if not port:
                self.__port = 21             
            #open
            self.__t = FTP()
            self.__t.connect(self.__hostname, self.__port, self.__timeout)                                 
        elif self.__typeProtocol == 'sftp':    
            if not port:
                self.__port = 22
            #open
            self.__ssh = paramiko.Transport((self.__hostname, self.__port))
                                                                
    def connection(self, username, password):
        """
        Connect to the remote server using provided username and password.

        Parameters:
        username (str): The username to use for connecting to the remote server.
        password (str): The password to use for connecting to the remote server.

        Returns:
        None
        """
        if self.__typeProtocol == 'ftp':
            self.__t.login(username, password)
            #default directory
            self.__defaultDirectory = self.__t.pwd()
        elif self.__typeProtocol == 'sftp':
            self.__ssh.connect(username = username, password = password)            
            self.__t = paramiko.SFTPClient.from_transport(self.__ssh)                                        
            self.__t.sock.settimeout(self.__timeout)
            #default directory
            self.__defaultDirectory = None
    
    def get(self,  filename, remoteDirectory=None, localDirectory=None):
        """
        This method is used to retrieve a file from a remote directory and save it to a local directory.    
        :param filename: The name of the file to be retrieved.
        :type filename: str
        :param remoteDirectory: The remote directory where the file is located. (default: None)
        :type remoteDirectory: str
        :param localDirectory: The local directory where the file will be saved. (default: None)
        :type localDirectory: str        
        :return: None
        """        
        if localDirectory is None:
            localDirectory = os.path.dirname(os.path.realpath(__file__))
        
        if self.__typeProtocol == 'ftp':
            pwdAux = self.__t.pwd()            
            if remoteDirectory is not None: 
                self.__t.cwd(remoteDirectory)
            remoteFile = open(os.path.join(localDirectory, filename), 'wb').write
            self.__t.retrbinary("RETR " + filename, remoteFile)            
            self.__t.cwd(pwdAux)    
            remoteFile.close()
        elif self.__typeProtocol == 'sftp':              
            if remoteDirectory is not None:
                self.__t.chdir(remoteDirectory)                
            self.__t.get(filename, os.path.join(localDirectory, filename))
            self.__t.chdir(None)            
            
    def put(self, filename, remoteDirectory=None, localDirectory=None):
        """
        Upload a file to remote directory. If remote directory is not provided, upload to current working directory.
        If local directory is not provided, upload from current working directory.
        :param filename: name of the file to upload
        :type filename: str
        :param remoteDirectory: (optional) remote directory to upload file to
        :type remoteDirectory: str
        :param localDirectory: (optional) local directory to upload file from
        :type localDirectory: str
        """
        if localDirectory is None:
            localDirectory = os.path.dirname(os.path.realpath(__file__))
                    
        if self.__typeProtocol == 'ftp':
            pwdAux = self.__t.pwd()
            if remoteDirectory is not None:
                self.__t.cwd(remoteDirectory)                
            localFile = open(filename, 'r')
            self.__t.storbinary('RETR %s' % filename, localFile.write)
            self.__t.cwd(pwdAux)
            localFile.close()
        elif self.__typeProtocol == 'sftp':            
            if remoteDirectory is not None:
                self.__t.chdir(remoteDirectory)
            self.__t.put(os.path.join(localDirectory, filename), filename)        
            self.__t.chdir(None)
            
    def disconnect(self):
        """
        This method disconnects the current connection.
        """
        if self.__typeProtocol == 'ftp':
            self.__t.quit()       
        elif self.__typeProtocol == 'sftp':
            self.__t.close()
            self.__ssh.close()
          
    def pwd(self):
        """
        Returns the current working directory of the connection.
        """
        if self.__typeProtocol == 'ftp':
            return self.__t.pwd()       
        elif self.__typeProtocol == 'sftp':
            return self.__t.getcwd()
        
    def cwd(self, remoteDirectory = None):
        """
        Changes the current working directory of the connection.
        """
        if self.__typeProtocol == 'ftp':
            self.__t.cwd(remoteDirectory)      
        elif self.__typeProtocol == 'sftp':
            self.__t.chdir(remoteDirectory) 
    
    def setDefaultDirectory(self):
        """
        Sets the current working directory to the default directory.
        """
        if self.__typeProtocol == 'ftp':
            self.__t.cwd(self.__defaultDirectory)    
        elif self.__typeProtocol == 'sftp':
            self.__t.chdir(None)
                
    def remotePathJoin (self, *paths):        
        """
        Returns separate paths  to string.
        """  
        if len(paths)== 0:
            return None
        if len(paths)== 1:
            return paths[0]
        else:
            path = paths[0]        
        for i in paths[1:]:
            path += self.__SEP + i          
        return path  
       
                         

t = PyFileTransfer('sftp', 'test.rebex.net', 'unix')
t.connection("demo", "password")
#t.get("WinFormClient.png", '/pub/example')
print(t.pwd())
t.cwd('pub/example')
print(t.pwd())
t.setDefaultDirectory()
print(t.pwd())
t.disconnect()