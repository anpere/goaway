import random
import os
import multiprocessing
import subprocess
import time
import yaml
import signal
import logging

import cmdserver
from cmdclient import CmdClient
from config import ClusterConfig
import globalvars
import threading
import pickle

logger = logging.getLogger(__name__)

max_tries = 3


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

        self.kill_servers()
        self._sync_servers()
        self._start_servers()

        serversAlive = self.check_servers()
        logger.debug("servers alive after started? %s" % (serversAlive))

    def _start_servers(self):
        """Start any servers which are local."""
        for user, host, port in self.server_addresses:
            if host == self.myaddress:
                logger.info("Starting local server %s %s", host, port)
                proc = multiprocessing.Process(
                    target=lambda: cmdserver.start_server(port=port, config=self._config))
                # https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Process.daemon
                proc.daemon = True
                proc.start()
            else:
                print "Starting remote server: %s:%s with config_path:%s" % (host, port, self.config_path)
                remoteHost = "%s@%s" % (user, host)
                command = "cd ~/goaway; DEBUG=true goaway/cmdserver.py %s" % (self.config_path)
                # command  = "cd ~/goaway ; goaway/foo.sh"
                ## subprocess.call blocks, while subprocces.Popen doesn't block.
                sshPopen = subprocess.Popen(["ssh", remoteHost, command], shell = False, stdout= subprocess.PIPE, stderr = subprocess.PIPE)

                ## Wait until server is up and running
                ##  while (not self._check_server(user, host, port)):
                ##      continue
                ##  print "server %s@%s:%s is up" %(user, host, port)


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
            print "rsync -r %s %s:%s" % (src_path, user+"@"+host, trg_path)
            os.system('rsync -r --exclude "%s" "%s" "%s:%s"' % (".git server.log", src_path, user + "@" + host, trg_path))
            print "done rysncing"

    def server_count(self):
        return len(self.server_addresses)

    def check_servers(self):
        allAlive = True
        for user, host, port in self.server_addresses:
            allAlive &= self._check_server(user, host, port)
        return allAlive


    ''' returns True if and only if the target server responds '''
    def _check_server(self, user, host, port):
        # Try each server a few times.
        for _ in xrange(max_tries):
            if CmdClient(user, host, port).check():
                return True
            time.sleep(.5)
        return False

    def kill_servers(self):
        logger.info("killing all servers")
        for user, host, port in self.server_addresses:
            self._kill_server(user, host, port)
        return

    def _kill_server(self, user, host, port):
        logger.info("killing %s:%s" % (host, port))
        result = CmdClient(user, host, port).kill()
        return

    def run_on_server(self, server_id, file_name, function_name, *args, **kwargs):
        user, host, port = self.server_addresses[server_id]
        print "running %s(%s) on %s:%s" % (function_name, args, host, port)
        result = CmdClient(user, host, port).run_remote(file_name, function_name, *args, **kwargs)
        return

    def goaway(self, file_name, function_name, *args, **kwargs):
        server_id = self.random_server_id()
        self.run_on_server(server_id, file_name, function_name, *args, **kwargs)


    def random_server_id(self):
        return random.randrange(0, len(self.server_addresses))
