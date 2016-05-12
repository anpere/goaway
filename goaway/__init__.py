import inspect
import random
import time
import signal
import sys
import logging

import logsetup
logsetup.setup()

import globalvars
import rpc
from remotecontrol import RemoteControl
from objectconstructors import *
from datastorehandle.weak import WeakDataStoreHandle
from datatypes import *
from datatypes.lock import Lock
from datastorehandle import *

logger = logging.getLogger(__name__)

## User runs this function to start off system
## probably will read the config file for info
## on cluster config, and maybe imports
def init(config_path):
    """
    Initiliazes a local spawner.
    On startup that spawner sets up the remote slaves.
    Args:
       config_path: string path of config file (see examples/example.yaml for an example config)
    """
    logger.debug("starting master ...")
    globalvars.rc = RemoteControl(config_path)
    globalvars.init_data_stores()
    ## Sets the hook for interrupts. This needs to happen after forking.
    ## If it happens before, every command server will execute the ctrl-c hook
    signal.signal(signal.SIGINT, globalvars.sigint)
    signal.siginterrupt(signal.SIGINT, False)

def goaway(fn, *args, **kwargs):
    """ fn is a function, not a string. Its args are *args & **kwargs """
    source = inspect.getsource(fn)
    name = fn.__name__
    file_name = inspect.getfile(fn)
    globalvars.rc.goaway(file_name, name, *args, **kwargs)
