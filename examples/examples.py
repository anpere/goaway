import sys
import os
""" Example uses of goaway. Cases to remember to handle."""
sys.path.append(os.path.abspath(os.path.join("../goaway")))
from goaway import *

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    init_master(config_path)

    """ Non-global reference """
    def f():
        def g():
            def h():
                return "hi"
            print h()
        goaway(g)

    """ Lambda expression """
    # Maybe we don't need this
    # The lambda wouldn't make sense to take args
    # So it could always be emulated by passing the args to goaway
    goaway(lambda: myobj.do_thing("args"))
