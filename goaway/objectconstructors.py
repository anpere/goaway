from objecthandle import ObjectHandle
from goaway.datastorehandle.strictcentralized import StrictCentralizedDataStoreHandle
import globalvars
import logging

logger = logging.getLogger(__name__)

class StrictCentralized(ObjectHandle):
    def __init__(self, name):
        ObjectHandle.__init__(self, globalvars.STRICT_CENTRALIZED_KIND, name)
