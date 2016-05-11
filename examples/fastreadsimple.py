"""
A very simple test of GoAway's fast read storage.

Owner: mlsteele
Status: Works.
"""
import sys
import os
import time
import random

import goaway
import common

fast = goaway.LinFastRead("fast")

if __name__ == "__main__":
    config_path = common.select_config()

    # Initialize GoAway.
    goaway.init(config_path)

    fast.x = 1
    print fast.x
    fast.x = 2
    print fast.x
    fast.x = 3
    print fast.x

    print "done"
