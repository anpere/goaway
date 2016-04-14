import time

from remotecontrol import RemoteControl

rc = RemoteControl(myaddress="localhost")

print "Server count", rc.server_count()

def run_remote_verbose(server_id, function_name, arg):
    print "-> Running {}({}) on server {}".format(function_name, arg, server_id)
    rc.run_on_server(server_id, function_name, arg)
    print "<- Remote thread started"

run_remote_verbose(0, "square", 2)
run_remote_verbose(1, "cube", 2)
run_remote_verbose(2, "sqrt", 2)

run_remote_verbose(rc.random_server_id(), "square", 3)

time.sleep(3)
