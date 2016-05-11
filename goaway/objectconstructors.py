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
    """
    Represents an object who accesses satisfy release consistency
    Each object has a lock which is used to cooridinate with copies
    of that object on different machines.
    Changes made to the object are propogated when that object's lock has
    been released
    """
    def __init__(self, name):
        self.__dict__[LOCK_ATTR] = Lock(name)
        ## buffer which contains the operations
        self.__dict__[BUFFER_ATTR] = []
        ObjectHandle.__init__(self, globalvars.RELEASE_KIND, name)
        store = globalvars.get_data_store(getattr(self, DATA_STORE_HANDLE_KIND_ATTR))
        store.make_object(name)

    def acquire(self):
        ## 1. Acquire the object's lock
        store = globalvars.get_data_store(getattr(self, DATA_STORE_HANDLE_KIND_ATTR))
        object_name = getattr(self, NAME_ATTR)
        store.acquire(object_name)

    def release(self):
        store = globalvars.get_data_store(getattr(self, DATA_STORE_HANDLE_KIND_ATTR))
        object_name = getattr(self, NAME_ATTR)
        store.release(object_name)
>>>>>>> wrote updateonrelease object and datastore
