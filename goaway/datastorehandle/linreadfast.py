import logging
import requests
import threading
import collections
import time

import goaway.globalvars as globalvars
import goaway.rpc as rpc
from goaway.common import RpcException
from goaway.datastorehandle.datastorehandle import DataStoreHandle

logger = logging.getLogger(__name__)

Entry = collections.namedtuple("Entry", ["value", "locked"])
# value: the value of the object.
# writing: Boolean as to whether a write is occurring. This is semantically a lock.

class LinReadFastDataStoreHandle(DataStoreHandle):
    """A maybe-serializable data store optimized for reads.
    TODO not linearizable. rename.

    All (name, field) values in this datastore default to None.

    Every node stores a local copy of all data.
    Reads can be executed locally and will walways return immediately.
    Whenever a write is issued, a two-phase locking commit occurs:
      1. The object is frozen at all nodes. (expanding phase)
      2. The object is updated and unfrozen at all nodes. (shrinking phase)
    The phases occur in the order the servers are listed in config.all_servers.
    Compromises have been made so that no operations actually block except for client set.
    """
    def __init__(self):
        # key: tuple of (name, field)
        # value: Entry
        self.data = {} # key: name of object; value: object dict
        # Lock to make access threadsafe.
        self.data_lock = threading.RLock()

    def get(self, name, field):
        """Get a value from the datastore.
        Reads from the local store.
        Always returns immediately.
        Args:
           name: name of object in datastore.
           field: field of the object in datastore
        """
        with self.data_lock:
            entry = self.data.get((name, field))
            if entry:
                return entry.value
            else:
                return None

    def set(self, name, field, value):
        """Set a value in the datastore.
        Blocks but for a bounded time assuming the system is correct.
        Args:
           name: name of object in datastore
           field: field of the object in datastore
           value: value to set the field of object
        """
        server_addresses = globalvars.config.all_servers

        # Lock the object on all servers.
        for addr in server_addresses:
            self._acquire_lock_sync(addr, name, field)

        # Send the update to all servers.
        for addr in server_addresses:
            self._send_update_sync(addr, name, field, value)

    def _acquire_lock_sync(self, server_address, name, field):
        """Acquire object write-lock on a server.
        Uses polling to avoid blocking anything.
        This leads to network saturation, but is a tradeoff we chose.
        Returns once the lock has been acquired.
        """
        while True:
            payload = {
                "consistency": globalvars.LIN_READ_FAST_KIND,
                "name": name,
                "field": field,
            }
            resj = rpc.rpc("POST", self._server_url(server_address, "/serreadfast/acquire"), payload)

            if resj.get("success") == True:
                return

            time.sleep(.1)


    def _send_update_sync(self, server_address, name, field, value):
        """Send the new value and release the write-lock on a server.
        Guaranteed to succeed immediately. (in the absence of network failures)
        """
        payload = {
            "consistency": globalvars.LIN_READ_FAST_KIND,
            "name": name,
            "field": field,
            "value": value,
        }
        resj = rpc.rpc("POST", self._server_url(server_address, "/serreadfast/update"), payload)
        assert resj.get("success") == True

    def _on_acquire(self, name, field):
        """Receiver for acquire requests.
        Returns: Boolean whether the acquire succeeded.
        """
        with self.data_lock:
            entry = self.data.get((name, field))
            if not entry:
                entry = Entry(None, False)
                self.data[(name, field)] = entry

            if entry.locked:
                return False
            else:
                self.data[(name, field)] = entry._replace(locked=True)
                return True

    def _on_update(self, name, field, value):
        """Receiver for update requests.
        Updates the object value and releases the lock.
        """
        with self.data_lock:
            self.data[(name, field)] = Entry(value, False)

    def _server_url(self, server_address, url_subpath):
        """Create a URL for contacting a server."""
        # The data master is the first server listed in the config.
        return "http://{}:{}/{}".format(server_address.host, server_address.port, url_subpath)
