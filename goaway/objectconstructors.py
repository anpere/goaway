from objecthandle import ObjectHandle
from globalvars import strictCentralizedDataStoreHandle

class StrictCentralized(ObjectHandle):
    def __init__(self, name):
        ObjectHandler.__init__(self, strictCentralizedDataStoreHandle, name)

