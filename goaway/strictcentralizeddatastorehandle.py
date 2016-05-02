import requests

import globalvars
from common import RpcException
from datastorehandle import DataStoreHandle


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

        pass

    def create(self, name, default):
        """Creates a strict object in the datastore.
        Args:
            name: name of object in datastore.
        """
        payload = {
            "consistency": "strict",
            "name": name,
        }
        resj = self._rpc("POST", self._master_url("data/create"), payload)


    def get(self, name, field):
        """Get a value from the datastore.
        Args:
           name: name of object in datastore.
           field: field of the object in datastore
        """
        payload = {
            "consistency": "strict",
            "name": name,
            "field": field
        }
        resj = self._rpc("GET", self._master_url("data/get"), payload)
        return resj["value"]

    def set(self, name, field, value):
        """Set a value in the datastore.
        value must be json-encodable.
        Args:
           name: name of object in datastore
           field: field of the object in datastore
           value: value to set the field of object
        """
        payload = {
            "consistency": "strict",
            "name": name,
            "field": field,
            "value": value,
        }
        resj = self._rpc("POST", self._master_url("data/set"), payload)

    def _rpc(self, http_method, url, payload):
        """Issue an rpc.
        Raises if "error" is a key in the response.
        Returns the json response.
        Args:
            http_method: One of "GET" or "POST".
            url: Url to send the request to.
            payload: Payload to send with request.
        """
        if globalvars.config == None:
            raise RuntimeError("globalvars.config not yet initialized.")
        try:
            if http_method == "GET":
                res = requests.get(url, json=payload)
            elif http_method == "POST":
                res = requests.post(url, json=payload)
            else:
                raise RuntimeError("Unsupported HTTP type {}".format(http_method))
        except Exception as ex:
            # TODO retry
            # TODO catch a less broad exception.
            raise RpcException("Could not connect to RPC server.", ex)
        if res.status_code != 200:
            raise RpcException("RPC server returned code {}".format(res.status_code))
        resj = res.json()
        if "error" in resj:
            if resj["error"] != "ok":
                raise RpcException(resj["error"])
        return resj

    def _master_url(self, url_subpath):
        """Create a URL for contacting the data master."""
        # The data master is the first server listed in the config.
        master_server = globalvars.config.servers[0]
        return "http://{}:{}/{}".format(master_server.host, master_server.port, url_subpath)
