from objecthandle import ObjectHandle
from strictcentralizeddatastorehandle import StrictCentralizedDataStoreHandle
import globalvars
import logging

logger = logging.getLogger(__name__)

class StrictCentralized(ObjectHandle):
    def __init__(self, name):
        self.create_datastore()
        ObjectHandle.__init__(self, globalvars.strictCentralizedDataStoreHandle, name)

    def create_datastore(self):
        """
        Creates a datastore for itself if one hasn't been created
        """
        if globalvars.strictCentralizedDataStoreHandle == None:
            globalvars.strictCentralizedDataStoreHandle = StrictCentralizedDataStoreHandle()
