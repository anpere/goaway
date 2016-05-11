import threading
from datastorehandle import DataStoreHandle

class WeakCentralizedDataStoreHandle(DataStoreHandle):
    def __init__(self):
        self.data = {}
        self.data_lock = threading.RLock()

    def create(self, name):
        """ Client requests to create an object """
        with self.data_lock:
            if not name in data:
                self.data[name] = {}
                self._create_remote(name)

    def _create_remote(self, name):
        """ Propagate the create to the master """
        payload = {
                "consistency": "weak",
                "name": name
        }
        threading.Thread(lambda:rpc.rpc("POST", rpc.master_url("data/create"), payload)).start()

    def receive_create(self, name):
        """ Receive a propagated create from the master """
        with self.data_lock:
            if not name in data:
                self.data[name] = {}

    def get(self, name, field):
        """ Client requests to get (no need to do remote action) """
        with self.data_lock:
            try:
                return self.data[name][field]
            except KeyError:
                raise AttributeError("Object<{}> has no such attribute '{}'".format(name, field))

    def set(self, name, field, value):
        """ Client requests to set """
        with self.data_lock:
            try:
                self.data[name][field] = value
                self._set_remote(name, field, value)
            except KeyError:

    def _set_remote(self, name, field, value):
        """ Propagate the set to all servers """
        pass

    def receive_set(self, name, field, value):
        """ Receive a propagated set from another server """
        pass
