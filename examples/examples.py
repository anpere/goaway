""" Example uses of goaway. Cases to remember to handle."""
from goaway.goaway import *

if __name__ == "__main__":
    init_master()

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
