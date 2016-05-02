from objecthandle import ObjectHandle
from globalvars import strictCentralizedDataStoreHandle

class StrictCentralized(ObjectHandle):
    def __init__(self, name):
        ObjectHandle.__init__(self, strictCentralizedDataStoreHandle, name)
