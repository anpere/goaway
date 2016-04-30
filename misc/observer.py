class SimpleStore(object):
    """Dead simple storage. Basically a dictionary."""
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value


class Observer(object):
    """
    Slightly magical object on which you can set any attributes.
    Prints to stdout all operations.
    Uses the get and set methods of the store argument.
    Just... don't mess with __store from the outside.
    """
    def __init__(self, store):
        self.__dict__["__store"] = store

    def __getattr__(self, name):
        store = getattr(self, "__store")
        value = store.get(name)
        print "get({}) -> {}".format(name, value)
        return value

    def __setattr__(self, name, value):
        store = getattr(self, "__store")
        print "set({}) <- {}".format(name, value)
        store.set(name, value)


store = SimpleStore()
o = Observer(store)

# Annoyingly, store is accessible from the outside.
print o.__store

o.x = "absolutely"
print o.x + " not"
print o.x * 5
o.x *= 3
print o.x
