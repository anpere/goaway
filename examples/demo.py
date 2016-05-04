import sys
import os
sys.path.append(os.path.abspath(os.path.join("../goaway")))
from goaway import *
import os
import math
import time

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
    ## TODO: make a similar test but with our recent specification
    ## The path or key is the address of the shared value.
    ##  data_path = "tweedle_dee_value_path"
    ## Ensure that the shared variable exists.
    ##create(data_path, default="")
    # Fetch the old value.
    ##old_value = get(data_path)
    # Append the argument.
    ##new_value = old_value + append_string
    # Save the new value to the datastore.
    ## set(data_path, new_value)

if __name__ == "__main__":
    if os.environ.get("GOAWAYPATH") == None:
        print "Goaway requires that you set $GOAWAYPATH. Otherwise it would rsync stuff willy nilly."
        sys.exit(1)
    if len(sys.argv) != 2:
        print "Usage: demo.py <place>"
        sys.exit(1)
    place = sys.argv[1]
    if place=="remote":
        config_name = "remote.yaml"
    elif place=="local":
        config_name = "local.yaml"
    elif place=="all":
        config_name = "config.yaml"
    else:
        sys.exit("expected locality argument to be either all, remote, or local")
        config_string
    config_path = os.path.join(os.path.dirname(__file__), config_name)
    num_of_servers = 6

    init(config_path)
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

    ## Verify distributed shared memory works
    goaway(grow_shared, "mua")
    goaway(grow_shared, "ha")
    goaway(grow_shared, "haa")
    time.sleep(3)
    ## print create("tweedle_dee_value_path", default="LAST")
    print "And now for the final result:"
    ## print get("tweedle_dee_value_path")
