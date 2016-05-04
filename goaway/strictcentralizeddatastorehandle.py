import requests

import globalvars
import rpc
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
        resj = rpc.rpc("POST", rpc.master_url("data/create"), payload)


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
        resj = rpc.rpc("GET", rpc.master_url("data/get"), payload)
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
        resj = rpc.rpc("POST", rpc.master_url("data/set"), payload)
