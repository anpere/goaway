import sys
import os
sys.path.append(os.path.abspath(os.path.join("../goaway")))
from goaway import *
import os

if __name__ == "__main__":
   weak = StrictCentralized()
   weak.clients = {}
   weak.value = 1
