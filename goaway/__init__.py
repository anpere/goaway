import inspect
import random
import time
import globalvars
import signal
from remotecontrol import RemoteControl
## User runs this function to start off system
## probably will read the config file for info
## on cluster config, and maybe imports

def init_master(config_path):
    print "starting master ..."
    globalvars.rc = RemoteControl(config_path, "localhost")
    print "in init ref of rc %s" % (globalvars.rc.__hash__)
    serversAlive = globalvars.rc.check_servers()
    print "started master. serversAlive? %s" % (serversAlive)
    ## Sets the hook for interrupts. This needs to happen after forking.
    ## If it happens before, every command server will execute the ctrl-c hook
    signal.signal(signal.SIGINT, globalvars.sigint)
    signal.siginterrupt(signal.SIGINT, False)

def init_slave():
    pass

def goaway(fn, *args, **kwargs):
    """ fn is a function, not a string. Its args are *args & **kwargs """
    source = inspect.getsource(fn)
    name = fn.__name__
    print "goaway is calling %s(%s, %s)" % (fn.__name__, args, kwargs)
    ## TODO: probably take a pickled function
    file_name = inspect.getfile(fn)
    print "in goaway ref of rc %s" % (globalvars.rc.__hash__)
    print "at least one server alive before goaway call? %s" % (globalvars.rc.check_servers())
    globalvars.rc.goaway(file_name, name, *args, **kwargs)
