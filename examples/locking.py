"""
A test of GoAway locks.
Increments a counter guarded by a lock 10 times.

Owner: jessk
Status: Works
"""
import sys
import os
from time import sleep

import goaway
import common

l = goaway.Lock("l")
s = goaway.StrictCentralized("s")

def increment_and_copy():
    l.acquire()
    s.num += 1
    s.num2 = s.num
    l.release()

if __name__ == "__main__":
    config_path = common.select_config()

    # Initialize GoAway.
    goaway.init(config_path)
    s.num = 0

    for i in range(10):
        goaway.goaway(increment_and_copy)

    while s.num < 10:
        sleep(.05)

    r1 = s.num
    r2 = s.num2

    print "Result num", r1
    print "Result num2", r2

    assert(r1 == 10)
    assert(r2 == 10)
