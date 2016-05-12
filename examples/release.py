"""
TODO description
Status: in-progress
"""

import sys
import os
from time import sleep

import goaway

rc = goaway.UpdateOnRelease("rc")

def inc_and_dec():
    rc.acquire()
    rc.x += 1
    rc.y -=1
    rc.release()

if __name__ == "__main__":

    # Initialize GoAway.
    goaway.init(os.path.join(os.path.dirname(__file__), 'remote.yaml'))
    rc.acquire()
    rc.x = 0
    rc.y = 10
    rc.release()
    x_goal = 10
    y_goal = 0

    for i in range(x_goal):
        goaway.goaway(inc_and_dec)

    sleep(10)

    x = rc.x
    y = rc.y
    assert x == x_goal, "expected %s, got %s" % (x_goal, x)
    assert y == y_goal, "expected %s, got %s" % (y, y_goal)
