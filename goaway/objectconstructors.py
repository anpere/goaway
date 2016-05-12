from objecthandle import ObjectHandle, NAME_ATTR
from goaway.datastorehandle.strictcentralized import StrictCentralizedDataStoreHandle
from goaway.datatypes.lock import Lock
import globalvars
import logging

logger = logging.getLogger(__name__)

class StrictCentralized(ObjectHandle):
    def __init__(self, name):
        ObjectHandle.__init__(self, globalvars.STRICT_CENTRALIZED_KIND, name)

class LinFastRead(ObjectHandle):
    def __init__(self, name):
        ObjectHandle.__init__(self, globalvars.LIN_FAST_READ_KIND, name)

class Weak(ObjectHandle):
    def __init__(self, name):
        ObjectHandle.__init__(self, globalvars.WEAK_KIND, name)

    def sync(self):
        globalvars.get_data_store(globalvars.WEAK_KIND).sync(getattr(self, NAME_ATTR))

class UpdateOnRelease(ObjectHandle):
    def __init__(self, name):
        ObjectHandle.__init__(self, globalvars.RELEASE_KIND, name)

    def acquire(self):
        ## 1. Acquire the object's lock
        globalvars.get_data_store(globalvars.RELEASE_KIND).acquire(getattr(self, NAME_ATTR))

    def release(self):
        globalvars.get_data_store(globalvars.RELEASE_KIND).release(getattr(self, NAME_ATTR))
