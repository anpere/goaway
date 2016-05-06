"""
A test of GoAway locks.

Owner: jessk
Status: Broken
"""
import sys
import os
from time import sleep

import goaway

l = goaway.Lock("l")
s = goaway.StrictCentralized("s")

def increment_and_copy():
    l.acquire()
    s.num += 1
    s.num2 = s.num
    l.release()

if __name__ == "__main__":
    # Find the config file.
    place  = sys.argv[1]
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

    # Initialize GoAway.
    goaway.init(config_path)
    s.num = 0

    for i in range(10):
        goaway.goaway(increment_and_copy)

    while s.num < 10:
        sleep(.05)

    r1 = s.num
    r2 = s.num2
    print "RESULT1", r1
    print "RESULT2", r2
