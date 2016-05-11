class DataStoreHandle(object):
    def __init__(self):
        pass

    def create(self, name):
        raise NotImplementedError("DataStoreHandle create")

    def get(self, name, field):
        raise NotImplementedError("DataStoreHandle get")

    def set(self, name, field, value):
        raise NotImplementedError("DataStoreHandle set")

