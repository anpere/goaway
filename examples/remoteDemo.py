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
def grow_shared(append_string):
    """Grow a shared string.
    Appends append_string to the shared string.
    This is not an atomic operation and may lose append_string.
    """
    # The path or key is the address of the shared value.
    data_path = "tweedle_dee_value_path"
    # Ensure that the shared variable exists.
    db.create(data_path, default="")
    # Fetch the old value.
    old_value = db.get(data_path)
    # Append the argument.
    new_value = old_value + append_string
    # Save the new value to the datastore.
    db.set(data_path, new_value)


if __name__ == "__main__":
    print "Goaway assumes you have defined $GOAWAYPATH to the path of the repo, and if not it will probably rsync things you don't want rsynced to a remote server"
    run = raw_input("Continue [y/N]")
    if run != 'y':
        sys.exit(0)
    config_path = os.path.join(os.path.dirname(__file__), "remote.yaml")
    num_of_servers = 3

    init_master(config_path)
    db = DataStore()
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
