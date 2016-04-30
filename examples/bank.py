import sys
import os
sys.path.append(os.path.abspath(os.path.join("../goaway")))
from goaway import *
import math
import time

if __name__ == "__main__":
    zoobars = Weak()
    zoobars.clients = {}
    foocoins = Strong()
    foocoins.clients = {}
    def transfer(database, sender, receiver, amount):
        database.clients[sender]-=amount
        database.clients[receiver]+=amount

    transfer(zoobars, "alyssa", "ben", 10)
    transfer(foocoins, "alyssa", "ben", 10)
