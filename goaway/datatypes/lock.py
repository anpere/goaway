""" a goaway lock """
import uuid
import thread
import goaway.globalvars as globalvars

class Lock(object):
    def __init__(self, name):
        self.uuid = uuid.uuid1() # Unique to the process (who is holding the lock)
        self.name = name # All acquires happen on the same name

    def acquire(self):
        """ blocks """
        data = {"uuid": self.uuid,
                "name": self.name}
        while True:
            resj = self._rpc("POST", self._master_url("lock/acquire"), data)
            if resj["ok"] == "true": #TODO sketchy string
                return

    def release(self):
        """ doesn't block """
        thread.start_new_thread(self._release_async())

    def _release_async(self):
        """ sends release notice """
        data = {"uuid": self.uuid,
                "name": self.name}
        resj = self._rpc("POST", self._master_url("lock/release"), data)
