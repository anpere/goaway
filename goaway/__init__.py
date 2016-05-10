import inspect
import random
import time
import globalvars
import signal
import sys
import logging

import logsetup
logsetup.setup()

from remotecontrol import RemoteControl
from objectconstructors import *
from weakdatastorehandle import WeakDataStoreHandle
from datatypes import *
from datastorehandle import *

logger = logging.getLogger(__name__)

# Silence requests logging.
logging.getLogger("requests").setLevel(logging.WARNING)

## User runs this function to start off system
## probably will read the config file for info
## on cluster config, and maybe imports
def init(config_path):
    """
    Initiliazes a master that runs locally.
    On startup that master wakes up its remote slaves
    And gives them a copy of the dsm object
    Args:
       config_path: string lists path of config file for slaves to use
       TODO: dsm: DataStore object to be shared across machines
    """
    logger.info("starting master ...")
    ##TODO AP: initialize in a weak objecthandle contsructor
    globalvars.weakDataStoreHandle = WeakDataStoreHandle()
    globalvars.rc = RemoteControl(config_path, "localhost")
    serversAlive = globalvars.rc.check_servers()
    logger.debug("started master. serversAlive? %s" % (serversAlive))
    ## Sets the hook for interrupts. This needs to happen after forking.
    ## If it happens before, every command server will execute the ctrl-c hook
    signal.signal(signal.SIGINT, globalvars.sigint)
    signal.siginterrupt(signal.SIGINT, False)

def goaway(fn, *args, **kwargs):
    """ fn is a function, not a string. Its args are *args & **kwargs """
    source = inspect.getsource(fn)
    name = fn.__name__
    # logger.debug("goaway is calling %s(%s, %s)" % (fn.__name__, args, kwargs))
    ## TODO: probably take a pickled function
    file_name = inspect.getfile(fn)
    globalvars.rc.goaway(file_name, name, *args, **kwargs)

def makeStrictCentralized(name):
    return StrictCentralized(name)
