"""
A demo of the Weak datastore protocol.
Values are consistent after calling sync().
"""
import sys
import os
from time import sleep

import goaway

s = goaway.Weak("s")

def write_a():
    s.a = 1
    s.sync()
    s.done_a = True

def write_bc():
    s.b = 1
    s.c = 1
    s.sync()
    s.done_b = True

if __name__ == "__main__":

    # Initialize GoAway.
    goaway.init(os.path.join(os.path.dirname(__file__), 'remote.yaml'))
    s.done_a = False
    s.done_b = False
    s.a = 0
    s.b = 0
    s.c = 0
    s.sync()

    goaway.goaway(write_a)
    goaway.goaway(write_bc)

    a = s.a
    b = s.b
    c = s.c

    print "We haven't synced or checked that goaways have finished, so anything could happen:"
    print "a =", a
    print "b =", b
    print "c =", c

    while not (s.done_a and s.done_b):
        sleep(.05)

    s.sync()

    a = s.a
    b = s.b
    c = s.c

    print "The only possible values now are a=1 b=1 c=1:"

    print "a =", a
    print "b =", b
    print "c =", c

    assert s.a == 1
    assert s.b == 1
    assert s.c == 1
