"""
Example showing what globals() and locals() do.
"""

import importnp
from pprint import pprint

def count(collection, element):
    """Count the number of occurrences of element in collection.
    Also print locals"""
    c = 0
    for e2 in collection:
        if element == e2:
            c += 1
    print "Locals from function level:"
    pprint(locals())
    return c

print "Globals:"
pprint(globals())
print

print "Locals from file level:"
pprint(locals())
print

assert count([1,2,3,2,3,2], 2) == 3
print

importnp.print_env(pprint, "imanarg")
print
