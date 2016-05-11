class UpdateOnReleaseDataStoreHandle(DataStoreHandle):
    """ Represents a datastore
        Ensures that accesses to the objects contained by this datastore
        satisfy the properties of release
    """
    Operation = collections.namedtuple("Operation", ["name", "field", "value"])
    def __init__(self):
        self.data = {}
        self.locks = {}
        self.buffers = {}
        assert globalvars.config != None

    def acquire(self, name):
        ## TODO: delete the operations buffer?
        self.locks[name].acquire()

    def release(self, name):
        ## 0. Get operations buffer
        operations = self.buffers[name]
        ## 1. propogate operations buffer to the rest of the servers
        payload = {
            "consistency": "update",
            "name": name,
            "operations" : operations,
        }

        for server_address in globalvars.config.all_other_servers:
            resj = rpc.rpc("POST", self._server_url(server_address, "/update"), payload)
        ## 2. clear buffer
        self.buffers[name] = []
        ## 3. Release the lock
        self.locks[name].release()

    def make_objet(self, name):
        self.locks[name] = Lock(name)
        self.buffers[name] = []

    def get(self, name, field):
        return self.data[name][field]

    def set(self, name, field, value):
        ## write to that object's local cache
        self.data[name][field] = value
        ## log the operation to that object's operation buffer
        object_buffer = self.buffer[name]
        object_buffer.append(Operation(name, field, value))
        self.buffer[name] = object_buffer

    def _server_url(self, server_address, url_subpath):
        return "http://{}:{}/{}".format(server_address.host, server_address.port, url_subpath)
