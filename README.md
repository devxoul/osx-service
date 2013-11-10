## Installation

```
$ git clone https://github.com/devxoul/osx-service.git
$ cd osx-service
$ python setup.py
```


## How to use

### Registered service list

```
$ service list
* [RUNNING] nginx
* [STOPPED] mysql
```

### Using a command

#### Command list

```
$ service nginx
Usage: nginx {restart|start|status|stop}
```

#### Command: start

```
$ sudo service nginx start
Password:
Starting nginx: nginx.
```


## Development

**osx-service** is writted in python. Just open any files in `/usr/local/etc/service/services/` directory and see how it looks.

All services are subclass of `Service`. Methods defined in service class are used as a command. Methods that of name starts with "_"(underscore) are not used as a command.