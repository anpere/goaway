""" a goaway lock """
import random
import threading
import thread
import uuid
import logging

import goaway.globalvars as globalvars
import goaway.rpc as rpc

logger = logging.getLogger(__name__)


class Lock(object):
    """A GoAway Lock.
    All locks are centralized for full ordering of acquire and releases.
    Supports usage as a context manager.
    """
    def __init__(self, name):
        self.name = name # All acquires happen on the same name
        logger.debug("lock init [%s] on process [%s]", self.name, globalvars.proc_uuid)

    def get_uuid(self):
        # Globally unique identifier of this (thread, process) tuple.
        return "{}:{}".format(globalvars.proc_uuid, str(thread.get_ident()))

    def acquire(self):
        """ blocks """
        data = {"uuid": self.get_uuid(),
                "name": self.name}
        while True:
            resj = rpc.rpc("POST", rpc.master_url("lock/acquire"), data)
            if resj["ok"] == "ok":
                return

    def release(self):
        """ doesn't block """
        thread = threading.Thread(target=self._release_sync)
        thread.daemon = True
        thread.start()

    def _release_sync(self):
        """ sends release notice """
        data = {"uuid": self.get_uuid(),
                "name": self.name}
        resj = rpc.rpc("POST", rpc.master_url("lock/release"), data)

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        # Propagate exceptions.
        return False
