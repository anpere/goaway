import sys
import os
import os
import math
import time

from goaway import *
import common

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

stringStrict = makeStrictCentralized("stringStrict")

def grow_shared(append_string):
    """Grow a shared string.
    Appends append_string to the shared string.
    This is not an atomic operation and may lose append_string.
    """
    stringStrict.value += append_string

if __name__ == "__main__":
    config_path = common.select_config()

    num_of_servers = 6

    init(config_path)
    ## Verifies goaway can run some straightforward functions
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
    stringStrict.value = ""
    goaway(grow_shared, "mua")
    goaway(grow_shared, "ha")
    goaway(grow_shared, "haa")
    time.sleep(3)
    print "And now for the final result:"
    print stringStrict.value
