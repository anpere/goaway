import threading
from datastorehandle import DataStoreHandle

class WeakDataStoreHandle(DataStoreHandle):
    def __init__(self):
        self.data = {}
        self.data_lock = threading.RLock()

        # Number of pending RPCs
        self.outgoing_lock = threading.RLock()
        self.outgoing = 0

    def _rpc(self, server, target, payload):
        if "value" in resp:
            return resp["value"]

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
                raise AttributeError("Object<{}> has no such attribute '{}'".format(name, field))
        return

    def _set_remote(self, name, field, value):
        """ Propagate the set to all servers """
        for server in globalvars.config.all_other_servers:
            threading.Thread(
                    target=lambda:self._set_remote_single(server, name, field, value)).start()

    def _set_remote_single(self, server, name, field, value):
        with self.outgoing_lock:
            self.outgoing += 1
        url = "http://{}:{}/data/set".format(server.host, server.port)
        payload = {
                "consistency": "weak",
                "name": name,
                "field": field,
                "value": value
        }
        rpc.rpc("POST", url, payload)
        with self.outgoing_lock:
            self.outgoing -= 1

    def receive_set(self, name, field, value):
        """ Receive a propagated set from another server """
        # WHAT IS GOING ON??
        # for now, just accept everything
        # TODO what is going on.

        with self.data_lock:
            try:
                self.data[name][field] = value
            except KeyError:
                self.data[name] = {field: value}


    # TODO need to flush, how does that work?
    # What goes here vs in objecthandle?
    # def start_flush(self, name)
    # def end_flush(self, name)
