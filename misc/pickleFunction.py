"""
See how pickles affect various functions
"""

import pickle

def printer(string):
    print string
    return string

def genericTest(function):
    pickledFunction = pickle.dumps(function)
    unpickledFunction = pickle.loads(pickledFunction)
    for attribute in dir(function):
        assert getattr(function, attribute) == getattr(unpickledFunction, attribute)
functions = [printer]
if __name__ == "__main__":
    for function in functions:
        genericTest(function)
