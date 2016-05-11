import threading
import logging
from time import sleep
from datastorehandle import DataStoreHandle
from goaway import globalvars, rpc

logger = logging.getLogger(__name__)

class WeakDataStoreHandle(DataStoreHandle):
    def __init__(self):
        self.data = {}
        self.data_lock = threading.RLock()

        # Number of pending RPCs
        self.outgoing_lock = threading.RLock()
        self.outgoing = {} # key: object name; value: number of outgoing
        self.syncing = {} # key: object name; value: boolean if syncing

    def _reg_name(self, name):
        with self.data_lock:
            if not name in self.data:
                self.data[name] = {}
        with self.outgoing_lock:
            if not name in self.outgoing:
                self.outgoing[name] = 0
        if not name in self.syncing:
            self.syncing[name] = False

    def get(self, name, field):
        """ Client requests to get (no need to do remote action) """
        with self.data_lock:
            try:
                return self.data[name][field]
            except KeyError:
                raise AttributeError("Object<{}> has no such attribute '{}'".format(name, field))

    def set(self, name, field, value):
        """ Client requests to set """
        self._reg_name(name)
        with self.data_lock:
            self.data[name][field] = value
        self._set_remote(name, field, value)
        return

    def _set_remote(self, name, field, value):
        """ Propagate the set to all servers """
        for server in globalvars.config.all_other_servers:
            threading.Thread(
                    target=self._set_remote_single, args=(server, name, field, value)).start()

    def _set_remote_single(self, server, name, field, value):
        while self.syncing[name]:
            sleep(0.005)
        with self.outgoing_lock:
            self.outgoing[name] += 1
        url = "http://{}:{}/data/set".format(server.host, server.port)
        payload = {
                "consistency": "weak",
                "name": name,
                "field": field,
                "value": value
        }
        rpc.rpc("POST", url, payload)
        with self.outgoing_lock:
            self.outgoing[name] -= 1

    def receive_set(self, name, field, value):
        """ Receive a propagated set from another server """
        self._reg_name(name)
        with self.data_lock:
            self.data[name][field] = value

    def sync(self, name):
        self._reg_name(name)
        self.syncing[name] = True
        while True:
            with self.outgoing_lock:
                if self.outgoing[name] == 0:
                    self.syncing[name] = False
                    return
            sleep(0.005)
