""" a goaway lock """
import uuid
import thread
import goaway.rpc as rpc
import goaway.globalvars as globalvars

class Lock(object):
    def __init__(self, name):
        self.uuid = uuid.uuid1() # Unique to the process (who is holding the lock)
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
            if resj["ok"] == "ok": #TODO sketchy string
                self.acquired = True
                return

    def release(self):
        """ doesn't block """
        if self.acquired:
            self.acquired = False
            thread.start_new_thread(self._release_async())

    def _release_async(self):
        """ sends release notice """
        data = {"uuid": self.uuid,
                "name": self.name}
        resj = rpc.rpc("POST", rpc.master_url("lock/release"), data)
