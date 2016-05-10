import sys
import time

import os
import pickle
sys.path.append(os.path.abspath(os.path.join("../goaway")))
from goaway.remotecontrol import RemoteControl
from goaway.datastore import DataStore


config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
print "Config path::", config_path
rc = RemoteControl(config_path, "localhost")
db = DataStore()

print "Server count", rc.server_count()

def run_remote_verbose(server_id, function_name, *args):
    print "-> Running {}({}) on server {}".format(function_name, args, server_id)
    rc.run_on_server(server_id, function_name, *args)
    print "<- Remote thread started"
run_remote_verbose(0, "square", (2))
run_remote_verbose(1, "cube", 2)
run_remote_verbose(2, "sqrt", 2)
for serverId in range(rc.server_count()):
    run_remote_verbose(serverId, "square", serverId)

run_remote_verbose(rc.random_server_id(), "grow_shared", "mua")
run_remote_verbose(rc.random_server_id(), "grow_shared", "ha")
run_remote_verbose(rc.random_server_id(), "grow_shared", "haa")

time.sleep(3)
print db.create("tweedle_dee_value_path", default="LAST")
print "And now, for the final result:"
print db.get("tweedle_dee_value_path")
