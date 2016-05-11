import logging
import requests
import threading

import goaway.globalvars as globalvars
import goaway.rpc as rpc
from goaway.common import RpcException
from goaway.datastorehandle.datastorehandle import DataStoreHandle
import goaway.localip as localip

logger = logging.getLogger(__name__)


class StrictCentralizedDataStoreHandle(DataStoreHandle):
    """ Represents a DataStore.

        Ensures that accesses to the objects contained by this datastore
        satisfy the properties of strict consistency, that is:
        It requires that if a [node] reads any [strictobject], the value
        returned by the read operation is the value written by the most
        recent write operation to that [strictobject].
        https://en.wikipedia.org/wiki/Consistency_model#Strict_consistency

    """
    def __init__(self):
        ## dictionary that store strict objects
        self.data = {} # key: name of object; value: object dict
        self.data_lock = threading.RLock()

        assert globalvars.config != None
        self.master_server_address = globalvars.config.spawner_server

        # Decide whether we are the data master for this store.
        self.is_master = self.master_server_address.host in (localip.ipv4_addresses() + localip.ipv6_addresses())

        # TODO delete this
        print "-" * 20
        logger.warn("is master %s", self.is_master)
        print "-" * 20

    def create(self, name):
        """Creates a strict object in the datastore.
        Args:
            name: name of object in datastore.
        """
        if self.is_master:
            with self.data_lock:
                self.data[name] = {}
                return

        payload = {
            "consistency": "strict",
            "name": name,
        }
        resj = rpc.rpc("POST", self._master_url("data/create"), payload)


    def get(self, name, field):
        """Get a value from the datastore.
        Args:
           name: name of object in datastore.
           field: field of the object in datastore
        """
        if self.is_master:
            try:
                with self.data_lock:
                    return self.data[name][field]
            except KeyError:
                raise AttributeError("Object<{}> has no such attribute '{}'".format(name, field))
        payload = {
            "consistency": "strict",
            "name": name,
            "field": field
        }
        resj = rpc.rpc("GET", self._master_url("data/get"), payload)
        return resj["value"]

    def set(self, name, field, value):
        """Set a value in the datastore.
        value must be json-encodable.
        Args:
           name: name of object in datastore
           field: field of the object in datastore
           value: value to set the field of object
        """
        if self.is_master:
            with self.data_lock:
                try:
                    self.data[name][field] = value
                except KeyError:
                    self.data[name] = {field: value}
            return

        payload = {
            "consistency": "strict",
            "name": name,
            "field": field,
            "value": value,
        }
        resj = rpc.rpc("POST", self._master_url("data/set"), payload)

    def _master_url(self, url_subpath):
        """Create a URL for contacting the data master."""
        # The data master is the first server listed in the config.
        master_server = self.master_server_address
        return "http://{}:{}/{}".format(master_server.host, master_server.port, url_subpath)
