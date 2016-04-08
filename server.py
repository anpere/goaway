import socket
import pickle
print "hello world"
HOST = 'localhost'
PORT = 50007
s = None

for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except socket.error as msg:
        s.close()
        s = None
        print msg
        continue
    break
if s is None:
    print "could not open Socket"
    sys.exit(1)
print 'here'
conn, addr = s.accept()
print 'connected by', addr
while 1:
    print "LOOP"
    data = conn.recv(1024)
    if not data: break
    package = pickle.loads(data)
    print package
    exec(package["function"])
    eval(package["name"]+"()")
conn.close()
