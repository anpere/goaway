import numpy as np

def print_env(pprint, somearg):
    """Print the globals and locals from here.
    Passes pprint to be obnoxious.
    """

    print "Globals from other file:"
    pprint(locals())
    print "(note the lack of __name__ and of count)"
    print

    print "Locals from function level in other file:"
    pprint(locals())
