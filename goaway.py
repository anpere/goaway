# Echo client program
import socket
import sys
import pickle

class FirstClassValue:
    def __init__(self, function, name):
        self.function = function
        self.name = name

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
s = None
if __name__ == "main":
    print "Hello"
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print 'could not open socket'
        sys.exit(1)
    #s.sendall('Hello, world')
    #file = open('injection.py', 'r')
    #s.sendall(file.read())
    #data = s.recv(1024)
    #print 'Received', repr(data)

## User runs this function to start off system
## probably will read the config file for info
## on cluster config, and maybe imports
def init():
    ## TODO:

def run(function, name):
    ## TODO: needs to interpret arguments
    print function
    exec(function)
    exec(name+"()")
    package = {}
    package["function"] = function
    package["name"] = name
    pickleString = pickle.dumps(package, -1)
    s.sendall(pickleString)
