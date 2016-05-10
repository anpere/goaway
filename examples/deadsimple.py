"""
Dead simple example of using GoAway.
This should always report success.
"""
import sys
import os
import time

import goaway
import common

goaway.logger.setLevel("CRITICAL")

s = goaway.StrictCentralized("s")

def set_shared(x):
    s.val = x

if __name__ == "__main__":
    config_path = common.select_config()

    goaway.init(config_path)

    print "Started."
    print "Setting val to 0."
    s.val = 0
    assert(s.val == 0)
    print "Starting goaway routine to set val to 5."
    goaway.goaway(set_shared, 5)
    print "Waiting for val to be non-zero..."
    while s.val == 0:
        print "Still waiting..."
        time.sleep(.05)
    print "Received non-0 value."
    assert(s.val == 5)
    print "Success."
