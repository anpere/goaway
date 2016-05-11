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
        store = globalvars.get_data_store(getattr(self, DATA_STORE_HANDLE_KIND_ATTR))
        object_name = getattr(self, NAME_ATTR)
        store.acquire(object_name)

    def release(self):
        store = globalvars.get_data_store(getattr(self, DATA_STORE_HANDLE_KIND_ATTR))
        object_name = getattr(self, NAME_ATTR)
        store.release(object_name)
