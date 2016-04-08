import goaway
import inspect

def printer():
    print "Hello, from the other side"

goaway.run(inspect.getsource(printer), printer.__name__)
