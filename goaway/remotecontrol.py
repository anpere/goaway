import random
import os
import multiprocessing
import time
import yaml

import cmdserver
from cmdclient import CmdClient


class RemoteControl(object):
    """Handle on remote goaway servers."""
    def __init__(self, myaddress=None):
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config_path, "r") as stream:
            self._config = yaml.load(stream)

        self.myaddress = myaddress
        self.server_addresses = map(_split_server_address, self._config["servers"])

        self._start_local_servers()

        self.check_servers()

    def _start_local_servers(self):
        """Start any servers which are local."""
        for host, port in self.server_addresses:
            if host == self.myaddress:
                print "Starting local server", host, port
                proc = multiprocessing.Process(
                    target=lambda: cmdserver.start_server(port=port))
                # https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Process.daemon
                proc.daemon = True
                proc.start()

    def server_count(self):
        return len(self.server_addresses)

    def check_servers(self):
        for host, port in self.server_addresses:
            self._check_server(host, port)

    def _check_server(self, host, port):
        # Try each server a few times.
        for _ in xrange(3):
            if CmdClient(host, port).check():
                return
            time.sleep(.5)

    def run_on_server(self, server_id, function_name, arg):
        host, port = self.server_addresses[server_id]
        result = CmdClient(host, port).run_remote(function_name, arg)
        return

    def random_server_id(self):
        return random.randrange(0, len(self.server_addresses))


def _split_server_address(server_string):
    """Split the likes of "18.5.5.5:9061" into ("18.5.5.5", 9061)."""
    split = server_string.split(":")
    assert len(split) == 2
    host, port = split[0], int(split[1])
    return host, port
