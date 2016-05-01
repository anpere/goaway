from objecthandle import ObjectHandle
from strictdatastore import StrictCentralizedDataStoreHandle

class StrictCentralized(ObjectHandle):
    def __init__(self, name):
        ObjectHandler.__init__(self, StrictCentralizedDataStoreHandle, name)

