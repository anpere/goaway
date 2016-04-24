import random
import os
import multiprocessing
import subprocess
import time
import yaml

import cmdserver
from cmdclient import CmdClient
from config import ClusterConfig
import globalvars


class RemoteControl(object):
    """Handle on remote goaway servers."""
    def __init__(self, myaddress=None):
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config_path, "r") as stream:
            self._config = ClusterConfig(yaml.load(stream))
            globalvars.config = self._config

        self.myaddress = myaddress
        self.server_addresses = self._config.servers
        self.file_paths = self._config.data["filepaths"]

        self._sync_servers()
        self._start_servers()

        self.check_servers()

    def _start_servers(self):
        """Start any servers which are local."""
        for user, host, port in self.server_addresses:
            if host == self.myaddress:
                print "Starting local server", host, port
                proc = multiprocessing.Process(
                    target=lambda: cmdserver.start_server(port=port, config=self._config))
                # https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Process.daemon
                proc.daemon = True
                proc.start()
            else:
                ret = subprocess.call(["ssh", user + "@"+ host, "~/goaway/cmdserver.py"])
                ## need to start a proc on a different machine
    def _sync_servers(self):
        for server_id in range(len(self.server_addresses)):
            user, host, port = self.server_addresses[server_id]
            if host != self.myaddress:
                self._sync_server(server_id)

    def _sync_server(self, server_id):
        user, host, port = self.server_addresses[server_id]
        for file_path in self.file_paths:
            os.system('scp "%s" "%s:%s"' % (file_path, user + "@" + host, file_path) )

    def server_count(self):
        return len(self.server_addresses)

    def check_servers(self):
        for user, host, port in self.server_addresses:
            self._check_server(user, host, port)

    def _check_server(self, user, host, port):
        # Try each server a few times.
        for _ in xrange(3):
            if CmdClient(user, host, port).check():
                return
            time.sleep(.5)

    def run_on_server(self, server_id, function_name, arg):
        user, host, port = self.server_addresses[server_id]
        result = CmdClient(user, host, port).run_remote(function_name, arg)
        return

    def random_server_id(self):
        return random.randrange(0, len(self.server_addresses))
