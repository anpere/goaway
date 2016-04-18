"""
Example uses of exec.

exec is a special form which takes 1, 2, or 3 arguments.
exec(expr, globals, locals)
locals and globals are optional.
expr is a string to be executed as code.
globals is a dictionary from symbol names to values.
locals is a dictionary from symbol names to values.
"""

import inspect
import numpy as np

def exec_verbose(expr, globalsd=None, localsd=None):
    """Wraps exec() and prints some stuff.
    Behaves just like exec with the following exceptions:
    - Prints the expr to be exec'd.
    - Catches and reports exceptions but does not throw.
    """
    # This line prints expr and whether or not global and locals exist.
    print "exec" + (" (g)" if globalsd != None else "") + (" (l)" if localsd != None else "") + ": " + expr
    try:
        if (globalsd == None) and (localsd == None):
            exec(expr)
        elif (globalsd != None) and (localsd == None):
            exec(expr, globalsd)
        elif (globalsd != None) and (localsd != None):
            exec(expr, globalsd, localsd)
        else:
            raise RuntimeError("bad exec_verbose args")
    except Exception as ex:
        print "exec failed:", type(ex).__name__, ex

a = 1
b = 2
print "Exec with implicit globals and locals."
exec_verbose("print a, b")
# 1 2
print

print "With empty globals."
exec_verbose("print a, b", {})
# exec failed: NameError name 'a' is not defined
print

print "With custom globals."
exec_verbose("print a, b", {"a": 3, "b": 4})
# 3 4
print

print "With shadowing of globals by locals."
exec_verbose("print a, b", {"a": 3, "b": 4}, {"b": 5})
# 3 5
print

print "Refer to imports within this file."
exec_verbose("print np.sin(0)")
# 0.0
print

print "Supplying globals kills imports."
exec_verbose("print np.sin(0)", {})
# exec failed: NameError name 'np' is not defined
print

print "You can simulate them."
exec_verbose("print np.sin(0)", {"np": np})
# 0.0
print

print "And do dirty tricks."
class FakeNumpy(object):
    def sin(self, x):
        return -1
print inspect.getsource(FakeNumpy).strip()
exec_verbose("print np.sin(0)", {"np": FakeNumpy()})
# -1
print
