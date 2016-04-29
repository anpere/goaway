import sys
import os
sys.path.append(os.path.abspath(os.path.join("../goaway")))
from goaway import *
import os
import math

def square(x):
    return x*x
def cube(x):
    return x*x*x
def sqrt(x):
    return x*.5
def add(a, b):
    return a + b
def addKey(a, b=0):
    return a+b
def mathSqrt(x):
    return math.sqrt(x)
if __name__ == "__main__":
    print "Goaway assumes you have defined $GOAWAYPATH to the path of the repo, and if not it will probably rsync things you don't want rsynced to a remote server"
    run = raw_input("Continue [y/N]")
    if run != 'y':
        sys.exit(0)
    config_path = os.path.join(os.path.dirname(__file__), "remote.yaml")
    num_of_servers = 3

    init_master(config_path)

    goaway(square, 1)
    goaway(cube, 2)
    goaway(sqrt, 3)
    ## Makes sure another function can run on another machine
    for i in range(num_of_servers):
        goaway(square, i)
    ## Verify goaway can run a function that takes multiple arguments on another machine
    for i in range(num_of_servers):
        goaway(add, i, 1)
        goaway(add, i, 2*i)
    ## Verify goaway can run a function that takes keyword arguments on another machine
    for i in range(num_of_servers):
        goaway(addKey, i)
        goaway(addKey, i, b=2*i)
    ## Verify goaway can run a function that imports another library another machine
    for i in range(num_of_servers):
        goaway(mathSqrt, i)
## run_remote_verbose(rc.random_server_id(), "grow_shared", "mua")
## run_remote_verbose(rc.random_server_id(), "grow_shared", "ha")
## run_remote_verbose(rc.random_server_id(), "grow_shared", "haa")
##
## time.sleep(3)
## print db.create("tweedle_dee_value_path", default="LAST")
## print "And now, for the final result:"
## print db.get("tweedle_dee_value_path")
