import sys
import os

from goaway import *
import common

if __name__ == "__main__":
    config_path = common.select_config()

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
