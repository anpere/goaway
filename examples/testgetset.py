import sys
import os
sys.path.append(os.path.abspath(os.path.join("../goaway")))
from goaway import *
import time

foobars = StrictCentralized("foobars")
print foobars.__hash__
def setandget(amount):
    """
    Set foobars.value to the given argument
    """
    foobars.value = amount
    return foobars.value

if __name__ == "__main__":
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
    init(config_path)
    goaway(setandget, 1)
    time.sleep(3)
    value = foobars.value
    assert value == 1, "foobars.value is wrong. expected 1, got %s" % (value)
