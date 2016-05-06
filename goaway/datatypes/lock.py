""" a goaway lock """
import random
import threading
import uuid
import goaway.rpc as rpc
import goaway.globalvars as globalvars

class Lock(object):
    def __init__(self, name):
        self.uuid = str(uuid.uuid4()) # Unique to the process (who is holding the lock)
        self.name = name # All acquires happen on the same name
        self.acquired = False # Whether I've currently got the lock

    def acquire(self):
        """ blocks """
        if self.acquired:
            return True # reentrant
        data = {"uuid": self.uuid,
                "name": self.name}
        while True:
            resj = rpc.rpc("POST", rpc.master_url("lock/acquire"), data)
            if resj["ok"] == "ok":
                self.acquired = True
                return

    def release(self):
        """ doesn't block """
        if self.acquired:
            self.acquired = False
            thread = threading.Thread(target=self._release_sync)
            thread.daemon = True
            thread.start()

    def _release_sync(self):
        """ sends release notice """
        data = {"uuid": self.uuid,
                "name": self.name}
        resj = rpc.rpc("POST", rpc.master_url("lock/release"), data)
