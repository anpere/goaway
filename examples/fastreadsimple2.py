"""
A very simple test of GoAway's fast read storage.

Owner: mlsteele
Status: Doesn't work.
"""
import sys
import os
import time
import random
import threading

import goaway
import common

fast = goaway.LinFastRead("fast")

def _run_in_thread(function, *args, **kwargs):
    """Run a function in a daemon thread."""
    thread = threading.Thread(target=function, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()

def monitor():
    while True:
        print fast.x
        time.sleep(.05)

if __name__ == "__main__":
    config_path = common.select_config()

    # Initialize GoAway.
    goaway.init(config_path)

    _run_in_thread(monitor)

    print "writing ->"
    fast.x = 1
    print "written <-"

    print "writing ->"
    fast.x = 2
    print "written <-"

    print "writing ->"
    fast.x = 3
    print "written <-"

    time.sleep(2)
    print "done"
