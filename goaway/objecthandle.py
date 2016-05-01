STORE_ATTR = "__store"
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
    def __init__(self, store, name):
        """
        Args:
            store: The DataStoreHandle to use to manage state.
            name: The unique identifier of the object.
        """
        self.__dict__[STORE_ATTR] = store
        self.__dict__[NAME_ATTR] = name

    def __getattr__(self, key):
        """
        Hook when an attribute is fetched.
        """
        store = getattr(self, STORE_ATTR)
        object_name = getattr(self, NAME_ATTR)
        object_value = store.get(object_name)
        try:
            val = object_value[key]
        except KeyError:
            raise AttributeError("Object<{}> has no such attribute '{}'"
                                 .format(object_name, key))
        return val

    def __setattr__(self, key, value):
        """
        Hook when an attribute is set.
        """
        store = getattr(self, STORE_ATTR)
        object_name = getattr(self, NAME_ATTR)
        store.set(object_name, key, value)
