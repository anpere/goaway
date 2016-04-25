def runner(function, *args, **kwargs):
    print args
    print kwargs
    result = function(*args, **kwargs)
    print result

def goaway(function, *args, **kwargs):
    runner(function, *args, **kwargs)

def badGoaway(function, *args, **kwargs):
    runner(function, args, kwargs)
def square(x):
    return x*x

def adder(a, b):
    return a+b

if __name__ == "__main__":
    print "normal runner"
    runner(square, 1)
    print "normal runner with two arguments"
    runner(adder, 1, 2)
    print "goaway: two levels of packing and unpacking"
    goaway(square, 1)
    print "badgoaway: two levels of packing and unpacking, but one done wrong"
    badGoaway(square, 1)
