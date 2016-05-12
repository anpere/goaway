from objecthandle import ObjectHandle, NAME_ATTR
from goaway.datastorehandle.strictcentralized import StrictCentralizedDataStoreHandle
from goaway.datatypes.lock import Lock
import globalvars
import logging

logger = logging.getLogger(__name__)

class StrictCentralized(ObjectHandle):
    def __init__(self, name):
        ObjectHandle.__init__(self, globalvars.STRICT_CENTRALIZED, name)

class UpdateOnRelease(ObjectHandle):
    def __init__(self, name):
       ObjectHandle.__init__(self, globalvars.RELEASE, name)

    def acquire(self):
        ## 1. Acquire the object's lock
        globalvars.get_data_store(globalvars.RELEASE).acquire(getattr(self, NAME_ATTR))

    def release(self):
        globalvars.get_data_store(globalvars.RELEASE).release(getattr(self, NAME_ATTR))

class LinFastRead(ObjectHandle):
    def __init__(self, name):
        ObjectHandle.__init__(self, globalvars.LIN_FAST_READ, name)

class Weak(ObjectHandle):
    def __init__(self, name):
        ObjectHandle.__init__(self, globalvars.WEAK, name)

    def sync(self):
        globalvars.get_data_store(globalvars.WEAK).sync(getattr(self, NAME_ATTR))
