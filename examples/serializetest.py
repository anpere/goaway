"""
See how various things look when serialized via pickle or inspect.
"""

import pickle
import inspect
import importnp

def f(x):
    """Takes a string and append '-g-f'
    Depends upon function g.
    """
    return g(x) + "-f"

def g(x):
    """Takes a string and append '-g'
    Does not depend on any other code.
    """
    return x + "-g"

print "Inspect serialize function."
# Printed with repr so that newlines show as "\n"
# which is less confusing when comparing formats.
print inspect.getsource(f).__repr__()
print

print "Pickle serialize function."
print pickle.dumps(f).__repr__()
print

print "Pickle serialize function from other module."
print pickle.dumps(importnp.print_env).__repr__()
print "It looks like it includes the name of the file (module) and function."
print

print "By the way, if define a function 'foo' in the REPL."
print "And then pickle it from the REPL, you will get this:"
print "c__main__\nfoo\np0\n.".__repr__()
print
