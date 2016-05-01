import unittest
import time
import sys, os
from goaway.remotecontrol import RemoteControl

rc = RemoteControl(myaddress="localhost")

print "Server count", rc.server_count()

def run_remote_verbose(server_id, function_name, arg):
    print "-> Running {}({}) on server {}".format(function_name, arg, server_id)
    rc.run_on_server(server_id, function_name, arg)
    print "<- Remote thread started"

class TestCreateFile(unittest.TestCase):
    def testCreateFile(self):
        for server in range(rc.server_count()):
            rc.run_on_server(server, "create", "test.txt")
            rc.run_on_server(server, "writeline", "hello, world!")

if __name__ == '__main__':
    unittest.main()
