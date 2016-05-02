import sys
import os
sys.path.append(os.path.abspath(os.path.join("../goaway")))
from goaway import *
import os

if __name__ == "__main__":
    ## TODO: ask Jess if this is correct
   zoobars = StrictCentralized("zoobars")
   zoobars.clients = {}
   zoobars.value = 1
