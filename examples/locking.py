"""
A test of GoAway locks.
Increments a counter guarded by a lock 10 times.
"""
import sys
import os
from time import sleep

import goaway

l = goaway.Lock("l")
s = goaway.StrictCentralized("s")

def increment_and_copy():
    with l:
        s.num += 1
        s.num2 = s.num

if __name__ == "__main__":
    # Initialize GoAway.
    goaway.init(os.path.join(os.path.dirname(__file__), 'remote.yaml'))
    s.num = 0
    s.num2 = 0
    goal = 10

    for i in range(goal):
        goaway.goaway(increment_and_copy)

    while s.num2 < goal:
        sleep(.05)

    r1 = s.num
    r2 = s.num2

    print "Result should be", goal, ":", r1
    print "Result 2 should also be", goal, ":", r2

    assert(r1 == goal)
    assert(r2 == goal)
