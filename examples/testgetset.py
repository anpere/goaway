import sys
import os
import time

from goaway import *
import common

foobars = StrictCentralized("foobars")
print foobars.__hash__
def setandget(amount):
    """
    Set foobars.value to the given argument
    """
    foobars.value = amount
    return foobars.value

if __name__ == "__main__":
    config_path = common.select_config()
    init(config_path)
    goaway(setandget, 1)
    time.sleep(3)
    value = foobars.value
    assert value == 1, "foobars.value is wrong. expected 1, got %s" % (value)
