import collections

import goaway.globalvars as globalvars
import goaway.rpc as rpc
from goaway.common import RpcException
from goaway.datastorehandle.datastorehandle import DataStoreHandle
import goaway.localip as localip
from goaway.datatypes.lock import Lock

Operation = collections.namedtuple("Operation", ["name", "field", "value"])
class UpdateOnReleaseDataStoreHandle(DataStoreHandle):
    """
    Represents an datastore that ensures accesses to objects in the data store
    satisfy the properties of release consistency
    Each object has a lock which is used to cooridinate with copies
    of that object on different machines.
    Changes made to the object are propogated when that object's lock has
    been released
    """
    def __init__(self):
        self.data = {}
        self.locks = {}
        self.buffers = {}
        assert globalvars.config != None

    def acquire(self, name):
        print "acquiring"
        try:
            self.locks[name].acquire
        except KeyError:
            self.locks[name] = Lock(name)
            self.buffers[name] = []
            self.locks[name].acquire()

    def release(self, name):
        ## 0. Get operations buffer
        print "releasing!!"
        operations = self.buffers[name]
        ## 1. propogate operations buffer to the rest of the servers
        payload = {
            "name": name,
            "operations" : operations,
        }

        for server_address in globalvars.config.all_other_servers:
            resj = rpc.rpc("POST", self._server_url(server_address, "updateonrelease/update"), payload)
        ## 2. clear buffer
        self.buffers[name] = []
        ## 3. Release the lock
        self.locks[name].release()

    def get(self, name, field):
        return self.data[name][field]

    def set(self, name, field, value):
        ## write to that object's local cache
        try:
            self.data[name][field] = value
        except KeyError:
            self.data[name] = {field:value}
            ## log the operation to that object's operation buffer
        try:
            object_buffer = self.buffers[name]
            object_buffer.append(Operation(name, field, value))
            self.buffers[name] = object_buffer
        except KeyError:
            self.buffers[name] = []
            self.buffers[name].append(Operation(name, field, value))

    def _server_url(self, server_address, url_subpath):
        return "http://{}:{}/{}".format(server_address.host, server_address.port, url_subpath)
