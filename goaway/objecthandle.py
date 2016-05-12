import logging

import goaway.globalvars as globalvars

logger = logging.getLogger(__name__)

DATA_STORE_HANDLE_KIND_ATTR = "__store"
NAME_ATTR = "__name"

class ObjectHandle(object):
    """
    Represents a shared object in a datstore.
    Instances of this class are returned by object handle constructors.
    Applications should not directly create these.

    Example:
        accumulators = goaway.StrictCentralized()
        accumulators.flowers = 0
        accumulators.trees = 10

    """
    def __init__(self, data_store_kind, name):
        """
        Args:
            data_store_kind: Name of the type of datastore to use (from globalvars)
            name: Name of the object, to identify its store.
        """
        self.__dict__[DATA_STORE_HANDLE_KIND_ATTR] = data_store_kind
        self.__dict__[NAME_ATTR] = name

    def __getattr__(self, field):
        """
        Hook when an attribute is fetched.
        """
        store = globalvars.get_data_store(getattr(self, DATA_STORE_HANDLE_KIND_ATTR))
        object_name = getattr(self, NAME_ATTR)
        value = store.get(object_name, field)
        return value

    def __setattr__(self, field, value):
        """
        Hook when an attribute is set.
        """
        store = globalvars.get_data_store(getattr(self, DATA_STORE_HANDLE_KIND_ATTR))
        object_name = getattr(self, NAME_ATTR)
        store.set(object_name, field, value)
