import inspect

## User runs this function to start off system
## probably will read the config file for info
## on cluster config, and maybe imports
def init_master():
    print "init master"
    pass

def init_slave():
    pass

def goaway(fn, *args, **kwargs):
    """ fn is a function, not a string. Its args are *args & **kwargs """
    source = inspect.getsource(fn)
    name = fn.__name__
    print name + " is going away...."
