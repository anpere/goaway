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
import threading
import pickle


class RemoteControl(object):
    """Handle on remote goaway servers."""
    def __init__(self, config_path, myaddress=None):
        with open(config_path, "r") as stream:
            self._config = ClusterConfig(yaml.load(stream))
            globalvars.config = self._config


        self.myaddress = myaddress
        self.config_path = config_path
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
                print "Starting remote server: %s:%s with config_path:%s" % (host, port, self.config_path)
                thread = threading.Thread(
                    target=lambda: subprocess.call(["ssh", user + "@"+ host, "~/goaway/goaway/run.sh $GOAWAYPATH/%s" % (self.config_path)]))
                thread.daemon = True
                thread.start()
                ## need to start a proc on a different machine
    def _sync_servers(self):
        for server_id in range(len(self.server_addresses)):
            user, host, port = self.server_addresses[server_id]
            if host != self.myaddress:
                self._sync_server(server_id)

    def _sync_server(self, server_id):
        user, host, port = self.server_addresses[server_id]
        for file_paths in self.file_paths:
            src_path, trg_path = file_paths.split(" ")
            print "rspnc -r %s %s:%s" % (src_path, user+"@"+host, trg_path)
            os.system('rsync -r --exclude "%s" "%s" "%s:%s"' % (".git", src_path, user + "@" + host, trg_path))

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

    def run_on_server(self, server_id, functionPickle, arg):
        user, host, port = self.server_addresses[server_id]
        depickledFunction = pickle.loads(functionPickle)
        function_name = depickledFunction.__name__
        function_module = depickledFunction.__module__
        print "running %s(%s) on %s:%s" % (function_name, arg, host, port)
        result = CmdClient(user, host, port).run_remote(function_module, function_name, arg)
        return

    def random_server_id(self):
        return random.randrange(0, len(self.server_addresses))
