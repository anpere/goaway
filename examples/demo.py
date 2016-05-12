"""
A few examples of different ways to call goaway
With args, with kwargs, using an imported module, etc...
"""
import sys
import os
import os
import math
import time

from goaway import *

def square(x):
    r = x*x
    mathStore.square = r
    return r

def cube(x):
    r = x*x*x
    mathStore.cube = r
    return r

def sqrt(x):
    r = x*.5
    mathStore.sqrt = r
    return r

def add(a, b):
    r = a + b
    mathStore.add = r
    return r

def addKey(a, b=0):
    r = a + b
    mathStore.addKey = r
    return r

def mathSqrt(x):
    r = math.sqrt(x)
    mathStore.mathSqrt = r
    return r

mathStore = StrictCentralized("mathStore")
stringStrict = StrictCentralized("stringStrict")

def grow_shared(append_string):
    """Grow a shared string.
    Appends append_string to the shared string.
    This is not an atomic operation and may lose append_string.
    """
    stringStrict.value += append_string

if __name__ == "__main__":

    num_of_servers = 6
    init(os.path.join(os.path.dirname(__file__), 'remote.yaml'))

    ## Verifies goaway can run some straightforward functions
    mathStore.square = None
    mathStore.cube = None
    mathStore.sqrt = None

    goaway(square, 1)
    goaway(cube, 2)
    goaway(sqrt, 3)

    while mathStore.square == None or mathStore.cube == None or mathStore.sqrt == None:
        pass
    assert mathStore.square == square(1)
    assert mathStore.cube == cube(2)
    assert mathStore.sqrt == sqrt(3)

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
    ## Note: This is not guaranteed to produce "muahahaa" because they may not be in order
    ## and some goaway may overwrite the result of another.
    stringStrict.value = ""
    goaway(grow_shared, "mua")
    goaway(grow_shared, "ha")
    goaway(grow_shared, "haa")
    print "Waiting for goaways to finish..."
    time.sleep(3)
    print "And now for the final result:"
    print stringStrict.value
