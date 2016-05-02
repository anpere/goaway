import sys
import os
sys.path.append(os.path.abspath(os.path.join("../goaway")))
from goaway import *
import os

if __name__ == "__main__":
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
    init_master(config_path)
    ## TODO: ask Jess if this is correct
    zoobars = StrictCentralized("zoobars")
    zoobars.clients = {}
    zoobars.value = 1
    alias = zoobars.clients
    alias[0] = 0
    zoobars.clients = alias

    # zoobars.clients["alyssa"] = 0
    zoobars.clients["ben"] = 1
