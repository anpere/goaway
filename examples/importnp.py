"""
This file exists to show what globals and locals look like
from the perspective of an imported file.
"""
import math as mathymath

def print_env(pprint, somearg):
    """Print the globals and locals from here.
    Passes pprint to be obnoxious.
    """

    print "Globals from other file:"
    globals2 = globals()
    globals2["__builtins__"] = "REDACTED"
    pprint(globals2)
    print "(note the lack of __name__ and of count)"
    print

    print "Locals from function level in other file:"
    pprint(locals())
