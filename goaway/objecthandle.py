import logging

logger = logging.getLogger(__name__)

DATA_STORE_HANDLE_ATTR = "__store"
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
    def __init__(self, dataStoreHandle, name):
        """
        Args:
            store: The DataStoreHandle to use to manage state.
            name: The unique identifier of the object.
        """
        logger.debug("datastore object:%s" % (dataStoreHandle.__hash__))
        self.__dict__[DATA_STORE_HANDLE_ATTR] = dataStoreHandle
        self.__dict__[NAME_ATTR] = name

    def __getattr__(self, field):
        """
        Hook when an attribute is fetched.
        """
        store = getattr(self, DATA_STORE_HANDLE_ATTR)
        object_name = getattr(self, NAME_ATTR)
        ## Field is not used in get intentionally
        ## zoobars.clients["a"] = 0
        ## money = zoobars.clients["a"]
        ## getattr has to return a dictionary so it can be keyed by "a"

        ## The cmdserver can return various types of data.
        ## The cmdserver can return an integer, or it can return a dictionary
        object_data = store.get(object_name, field)
        try:
            return object_data[field]
        except KeyError:
            raise AttributeError("Object<{}> has no such attribute '{}'"
                                 .format(object_name, field))

    def __setattr__(self, field, value):
        """
        Hook when an attribute is set.
        """
        store = getattr(self, DATA_STORE_HANDLE_ATTR)
        object_name = getattr(self, NAME_ATTR)
        store.set(object_name, field, value)
