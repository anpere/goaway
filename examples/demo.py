"""
A few examples of different ways to call goaway
With args, with kwargs, using an imported module, etc...
"""
import sys
import os
import os
import math
import time

import goaway

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

# Stores the results of our math operations
mathStore = goaway.StrictCentralized("mathStore")

if __name__ == "__main__":

    num_of_servers = 6
    goaway.init(os.path.join(os.path.dirname(__file__), 'remote.yaml'))

    ## Verifies goaway can run some straightforward functions
    mathStore.square = None
    mathStore.cube = None
    mathStore.sqrt = None

    goaway.goaway(square, 1)
    goaway.goaway(cube, 2)
    goaway.goaway(sqrt, 3)

    while mathStore.square == None or mathStore.cube == None or mathStore.sqrt == None:
        pass
    assert mathStore.square == square(1)
    assert mathStore.cube == cube(2)
    assert mathStore.sqrt == sqrt(3)
    print "Assertions passed!"

    ## Makes sure another function can run on another machine
    for i in range(num_of_servers):
        goaway.goaway(square, i)

    ## Verify goaway can run a function that takes multiple arguments on another machine
    for i in range(num_of_servers):
        goaway.goaway(add, i, 1)
        goaway.goaway(add, i, 2*i)

    ## Verify goaway can run a function that takes keyword arguments on another machine
    for i in range(num_of_servers):
        goaway.goaway(addKey, i)
        goaway.goaway(addKey, i, b=2*i)

    ## Verify goaway can run a function that imports another library another machine
    for i in range(num_of_servers):
        goaway.goaway(mathSqrt, i)

