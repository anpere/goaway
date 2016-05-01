""" a goaway lock """
import uuid, thread, globalvars

class Lock(object):
    def __init__(self):
        self.uuid = uuid.uuid1()
        self.d = StrictObjectHandle()
        self.d.

    def acquire(self):
        """ blocks """
        while True:
            resj = self._rpc("POST", self._master_url("lock/acquire"), {"uuid": self.uuid}))
            if resj["ok"] == "true": #TODO sketchy string
                return

    def release(self):
        """ doesn't block """
        thread.start_new_thread(self._release_async())

    def _release_async(self):
        """ sends release notice """
        resj
