import sys, os
sys.path.append(os.path.abspath(os.path.join("../goaway")))
import goaway
from time import sleep

s = goaway.StrictCentralized("s")

def increment():
    s.num += 1

if __name__ == "__main__":
    place  = sys.argv[1]
    if place=="remote":
        config_name = "remote.yaml"
    elif place=="local":
        config_name = "local.yaml"
    elif place=="all":
        config_name = "config.yaml"
    else:
        sys.exit("expected locality argument to be either all, remote, or local")
        config_string
    config_path = os.path.join(os.path.dirname(__file__), config_name)
    goaway.init(config_path)
    s.num = 0

    for i in range(10):
        goaway.goaway(increment)

    while s.num < 10:
        pass #wait

    r1 = s.num
    print "RESULT", r1
