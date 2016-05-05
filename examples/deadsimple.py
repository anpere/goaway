"""
Dead simple example of using GoAway.
This should always report success.
"""
import sys
import os
import goaway
import time

goaway.logger.setLevel("CRITICAL")

s = goaway.StrictCentralized("s")

def set_shared(x):
    s.val = x

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: deadsimple.py <place>"
        sys.exit(1)
    place = sys.argv[1]
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
