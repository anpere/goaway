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
    clients = GoawayDict()
    clients["hello"] = 1
    zoobars.clients = GoawayDict()
    zoobars.value = 1

    print "setting"
    zoobars.clients["alyssa"] = 0
    zoobars.clients["ben"] = 1
    zoobars.value +=1

    print "getting"
    assert zoobars.clients["alyssa"] == 0
    assert zoobars.clients["ben"] == 1
