import inspect
import random
import time
import globalvars
from remotecontrol import RemoteControl
## User runs this function to start off system
## probably will read the config file for info
## on cluster config, and maybe imports
def init_master(config_path):
    print "starting master ..."
    globalvars.rc = RemoteControl(config_path, "localhost")
    print "started master"
    pass

def init_slave():
    pass

def goaway(fn, *args, **kwargs):
    """ fn is a function, not a string. Its args are *args & **kwargs """
    source = inspect.getsource(fn)
    name = fn.__name__
    print "goaway is calling %s(%s, %s)" % (fn.__name__, args, kwargs)
    print
    ## TODO: probably take a pickled function
    file_name = inspect.getfile(fn)
    globalvars.rc.goaway(file_name, name, *args, **kwargs)
