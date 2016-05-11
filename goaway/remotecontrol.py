import random
import sys
import os
import multiprocessing
import subprocess
import time
import signal
import pickle
import logging
import threading

import cmdserver
from cmdclient import CmdClient
from config import ClusterConfig
import globalvars
import localip


logger = logging.getLogger(__name__)

max_tries = 3

# How long to wait for each server to start.
SERVER_START_TIMEOUT = 3.0


class RemoteControl(object):
    """Handle on remote goaway servers.
    Only instantiated on the spawner.
    """
    def __init__(self, config_path):
        self._config = ClusterConfig(config_path)
        globalvars.config = self._config
        logging.debug("using local  config path: %s", self._config.local_path)
        logging.debug("using remote config path: %s", self._config.remote_path)

        if self._config.spawner_server[1] not in (localip.ipv4_addresses() + localip.ipv6_addresses()):
            print "Spawner server is not one of your IPs."
            print "spawner ip from config: {}".format(self._config.spawner_server[1])
            print "local ips: {}".format(localip.ipv4_addresses())
            raise RuntimeError("spawner_server ip is not one of your ips", self._config.spawner_server[1])

        self.server_addresses = self._config.servers
        self.file_paths = self._config.data["filepaths"]

        self.kill_servers()
        self._sync_servers()
        self._start_servers()

        serversAlive = self.wait_for_servers(SERVER_START_TIMEOUT)
        if not serversAlive:
            raise RuntimeError("servers could not be started")

    def _start_servers(self):
        """Start all remote servers and one local server."""
        for user, host, port in self.server_addresses:
                remoteHost = "%s@%s" % (user, host)
                command = ("cd ~/goaway;" +
                        "find . -name '*.pyc' -delete ;" +
                        "DEBUG=true goaway/cmdserver.py %s %s %s >> server.std.log 2>&1" % (
                            host,
                            port,
                            self._config.remote_path,
                        ))
                logger.debug("Starting server:%s remoteHost with command:%s" % (remoteHost, command))
                ## subprocess.call blocks, while subprocces.Popen doesn't block.
                sshPopen = subprocess.Popen(["ssh", remoteHost, command],
                        shell = False, stdout= subprocess.PIPE, stderr = subprocess.PIPE)
        self._start_local_server()

    def _start_local_server(self):
        user, host, port = self._config.spawner_server
        logger.info("Starting local server %s:%s", host, port)
        thread = threading.Thread(
            target=lambda: cmdserver.start_server(port=port))
        # https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Process.daemon
        thread.daemon = True
        thread.start()

    def _sync_servers(self):
        for server_id in range(len(self.server_addresses)):
            self._sync_server(server_id)

    def _sync_server(self, server_id):
        user, host, port = self.server_addresses[server_id]
        for file_paths in self.file_paths:
            src_path, trg_path = file_paths.split(" ")
            src_path = src_path + "/"
            trg_path = trg_path + "/"
            if "$GOAWAYPATH" in src_path or  "$GOAWAYPATH" in trg_path:
                try:
                    os.environ["GOAWAYPATH"]
                except KeyError:
                    sys.exit("no goawaypath defined")
            rsync_command = 'rsync -r --exclude-from rsync_ignore.txt "%s" "%s:%s"' % (src_path, user + "@" + host, trg_path)
            logger.debug(rsync_command)
            os.system(rsync_command)
            logger.debug("done rysncing")

    def server_count(self):
        return len(self.server_addresses)

    def wait_for_servers(self, timeout):
        """Wait for all servers to become alive.
        Args:
            timeout: How long to wait for _each_ server before giving up.
        Returns: True if all servers are alive.
                 False if any server did not respond in time.
        """
        for user, host, port in self.server_addresses:
            if not self.wait_for_server(user, host, port, timeout):
                logging.warn("could not start server %s:%s:%s", user, host, port)
                return False
        return True

    def wait_for_server(self, user, host, port, timeout):
        time_start = time.time()
        while time.time() - time_start < timeout:
            if CmdClient(user, host, port).check():
                return True
        return False

    def kill_servers(self):
        logger.info("killing all servers")
        for user, host, port in self.server_addresses:
            self._kill_server(user, host, port)
        return

    def _kill_server(self, user, host, port):
        logger.info("killing %s:%s" % (host, port))
        result = CmdClient(user, host, port).kill()
        # Ignore the result of whether the server received the command.
        return

    def run_on_server(self, server_address, file_name, function_name, *args, **kwargs):
        user, host, port = server_address
        logger.debug("running %s(%s) on %s:%s" % (function_name, args, host, port))
        result = CmdClient(user, host, port).run_remote(file_name, function_name, *args, **kwargs)
        return

    def goaway(self, file_name, function_name, *args, **kwargs):
        server_address = self.random_server_address()
        self.run_on_server(server_address, file_name, function_name, *args, **kwargs)

    def random_server_address(self):
        i = random.randrange(0, len(globalvars.config.all_servers))
        return globalvars.config.all_servers[i]
