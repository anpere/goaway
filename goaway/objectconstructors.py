from objecthandle import ObjectHandle
import globalvars

class StrictCentralized(ObjectHandle):
    def __init__(self, name):
        print "in objconstructor:%s" % (globalvars.strictCentralizedDataStoreHandle.__hash__)
        ObjectHandle.__init__(self, globalvars.strictCentralizedDataStoreHandle, name)
