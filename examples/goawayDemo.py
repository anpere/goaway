import sys
import os
sys.path.append(os.path.abspath(os.path.join("../goaway")))
from goaway import *
import os

def square(x):
    return x*x
def cube(x):
    return x*x*x
def sqrt(x):
    return x*.5
def add(a, b):
    return a + b
if __name__ == "__main__":
    print "Goaway assumes you have defined $GOAWAYPATH to the path of the repo, and if not it will probably rsync things you don't want rsynced to a remote server"
    run = raw_input("Continue [y/N]")
    if run != 'y':
        sys.exit(0)
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    num_of_servers = 3

    init_master(config_path)

    goaway(square, 1)
    goaway(cube, 2)
    goaway(sqrt, 3)
    for i in range(num_of_servers):
         goaway(square, 2)

## run_remote_verbose(rc.random_server_id(), "grow_shared", "mua")
## run_remote_verbose(rc.random_server_id(), "grow_shared", "ha")
## run_remote_verbose(rc.random_server_id(), "grow_shared", "haa")
##
## time.sleep(3)
## print db.create("tweedle_dee_value_path", default="LAST")
## print "And now, for the final result:"
## print db.get("tweedle_dee_value_path")
