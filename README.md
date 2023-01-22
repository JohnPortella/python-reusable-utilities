This repository contains reusable modules for Python projects.

<br/>


# <a href="#custom-logging">Custom Logging</a>




## <kbd>function</kbd> `set_logger`

```python
set_logger(name, log_dir=None)
```

Initializes a logger with the given name and can write log messages to both stdout and a file in the specified log directory. 



**Args:**
 
 - <b>`name`</b> (str):  the name of the logger 
 - <b>`log_dir`</b> (str):  the directory where log files will be written, if None, only stdout is used 



**Returns:**
 
 - <b>`logging.Logger`</b>:  the initialized logger 


---

## <kbd>class</kbd> `LoggerFactory`
LoggerFactory is a class that inherits from the logging module's logger class and  allows for easy configuration and management of loggers. It has the following features: 
- Initializes a logger with a given name and set to debug level 
- Allows for adding of stream and file handlers 
- Provides methods for enabling/disabling console and file output 
- Automatically creates a log directory if it does not exist 
- File logs are saved with the date appended to the filename 

### <kbd>function</kbd> `__init__`

```python
__init__(name, log_dir=None)
```

:param name: name of the logger :type name: str :param log_dir: directory to save log files (default: None) :type log_dir: str 


---


### <kbd>function</kbd> `add_file_handler`

```python
add_file_handler(name, log_dir)
```

Adds a file handler to the logger :param name: name of the logger :type name: str :param log_dir: directory to save log files :type log_dir: str 

---

### <kbd>function</kbd> `disable_console_output`

```python
disable_console_output()
```

Disables console output for the logger 

---

### <kbd>function</kbd> `disable_file_output`

```python
disable_file_output()
```

Disables file output for the logger 

---

### <kbd>function</kbd> `enable_console_output`

```python
enable_console_output()
```

Enables console output for the logger 

---

### <kbd>function</kbd> `enable_file_output`

```python
enable_file_output()
```

Enables file output for the logger 

---

### <kbd>function</kbd> `generate_log_dir`

```python
generate_log_dir(log_dir)
```

Creates log directory if it does not exist :param log_dir: directory to save log files :type log_dir: str 

---

### <kbd>function</kbd> `has_console_handler`

```python
has_console_handler()
```

:return: True if the logger has a stream handler, False otherwise :rtype: bool 

---

### <kbd>function</kbd> `has_file_handler`

```python
has_file_handler()
```

:return: True if the logger has a file handler, False otherwise :rtype: bool 


---

## <kbd>class</kbd> `StaticLoggerFactory`
This class is a factory for creating a singleton instance of a logger. The logger is initialized with the given name and can write log messages to both stdout and a file in the specified log directory. 



**Attributes:**
 
 - <b>`_LOG`</b> (logging.Logger):  a singleton instance of a logger 

Methods: 
 - <b>`__new__`</b> (cls, name, log_dir=None):  creates and returns a singleton instance of a logger. The logger is initialized with the given name and can write log messages to both stdout and a file in the specified log directory. 

# <a href="#pyfile-transfer">Pyfile Transfer</a>

## <kbd>class</kbd> `PyFileTransfer`
A class for performing file transfer using FTP or SFTP.     

### <kbd>function</kbd> `__init__`

```python
__init__(
    typeProtocol='ftp',
    hostname='localhost',
    so='unix',
    port=None,
    timeout=None
)
```

Initializes the PyFileTransfer object and sets the connection parameters. 

**Args:**
 
 - <b>`typeProtocol`</b> (str):  'ftp' or 'sftp' protocol to use for the file transfer 
 - <b>`hostname`</b> (str):  the hostname or IP address of the server 
 - <b>`so`</b> (str):  'unix' or 'win' depending on the operating system of the server 
 - <b>`port`</b> (int):  the port number to use for the connection, if None it will use default port for the protocol 
 - <b>`timeout`</b> (int):  the timeout for the connection, if None it will use default timeout 




---


### <kbd>function</kbd> `connection`

```python
connection(username, password)
```

Connect to the remote server using provided username and password. 



**Parameters:**
 username (str): The username to use for connecting to the remote server. password (str): The password to use for connecting to the remote server. 



**Returns:**
 None 

---


### <kbd>function</kbd> `cwd`

```python
cwd(remoteDirectory=None)
```

Changes the current working directory of the connection. 

---

### <kbd>function</kbd> `disconnect`

```python
disconnect()
```

This method disconnects the current connection. 

---

### <kbd>function</kbd> `get`

```python
get(filename, remoteDirectory=None, localDirectory=None)
```

This method is used to retrieve a file from a remote directory and save it to a local directory.     :param filename: The name of the file to be retrieved. :type filename: str :param remoteDirectory: The remote directory where the file is located. (default: None) :type remoteDirectory: str :param localDirectory: The local directory where the file will be saved. (default: None) :type localDirectory: str         :return: None 

---

### <kbd>function</kbd> `put`

```python
put(filename, remoteDirectory=None, localDirectory=None)
```

Upload a file to remote directory. If remote directory is not provided, upload to current working directory. If local directory is not provided, upload from current working directory. :param filename: name of the file to upload :type filename: str :param remoteDirectory: (optional) remote directory to upload file to :type remoteDirectory: str :param localDirectory: (optional) local directory to upload file from :type localDirectory: str 

---

### <kbd>function</kbd> `pwd`

```python
pwd()
```

Returns the current working directory of the connection. 

---


### <kbd>function</kbd> `remotePathJoin`

```python
remotePathJoin(*paths)
```

Returns separate paths  to string. 

---

### <kbd>function</kbd> `setDefaultDirectory`

```python
setDefaultDirectory()
```

Sets the current working directory to the default directory. 

