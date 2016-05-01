import requests

import globalvars
from common import RpcException
from datastorehandle import DataStoreHandle


class StrictDataStoreHandle(DataStoreHandle):
    """A client to shared data storage.
    """
    def __init__(self):
        pass

    def create(self, path, default):
        """Ensure that a value exists in the datastore.
        Args:
            path: ID of data entry.
            default: Value to introduce _only_ if nothing existed there before.
        """
        payload = {
            "path": path,
            "default": default,
        }
        resj = self._rpc("POST", self._master_url("data/create"), payload)

    def get(self, path):
        """Get a value from the datastore."""
        payload = {
            "path": path,
        }
        resj = self._rpc("GET", self._master_url("data/get"), payload)
        return resj["value"]

    def set(self, path, value):
        """Set a value in the datastore.
        value must be json-encodable.
        """
        payload = {
            "path": path,
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
            raise RpcException(resj["error"])
        return resj

    def _master_url(self, url_subpath):
        """Create a URL for contacting the data master."""
        # The data master is the first server listed in the config.
        master_server = globalvars.config.servers[0]
        return "http://{}:{}/{}".format(master_server.host, master_server.port, url_subpath)
