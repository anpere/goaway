"""
A test of GoAway locks.
Increments a counter guarded by a lock 10 times.

Owner: anpere
Status: in-progress
"""

import sys
import os
from time import sleep

import goaway
import common

rc = goaway.UpdateOnRelease("rc")

def inc_and_dec():
    rc.acquire()
    rc.x += 1
    rc.y -=1
    rc.release()

if __name__ == "__main__":
    config_path = common.select_config()

    # Initialize GoAway.
    goaway.init(config_path)
    rc.x = 0
    x_goal = 10
    rc.y = -10
    y_goal = 0

    for i in range(x_goal):
        goaway.goaway(inc_and_dec)

    while rc.x < x_goal:
        sleep(.05)

    x = rc.x
    y = rc.y
    assert(x == x_goal)
    assert(y == y_goal)
