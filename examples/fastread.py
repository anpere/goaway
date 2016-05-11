"""
A test of GoAway's fast read storage.
A bunch of goaway threads issue many reads and a few writes.
They aggregate how long each one took.

Owner: mlsteele
Status: Works.
"""
import sys
import os
import time
import random

import goaway
import common

# How many reads and writes each worker issues.
NREADS = 1000
NWRITES = 10
NWORKERS = 5

# Lock to guard stats.
lock = goaway.Lock("lock")
# Statistic collected for reporting at the end.
stats = goaway.StrictCentralized("stats")
# Cache being tested for speed.
cache = goaway.LinFastRead("cache")

def worker(n):
    agenda = (["r"] * NREADS) + (["w"] * NWRITES)
    random.shuffle(agenda)
    read_time = 0.
    write_time = 0.
    for action in agenda:
        if action == "r":
            start_time = time.time()
            _ = cache.val
            end_time = time.time()
            read_time += end_time - start_time
        elif action == "w":
            start_time = time.time()
            cache.val = {"time": time.time()}
            end_time = time.time()
            write_time += end_time - start_time

    with lock:
        stats.read_time += read_time
        stats.read_count += NREADS
        stats.write_time += write_time
        stats.write_count += NWRITES
        stats.done += 1

if __name__ == "__main__":
    config_path = common.select_config()

    # Initialize GoAway.
    goaway.init(config_path)

    stats.read_time = 0
    stats.read_count = 0
    stats.write_time = 0
    stats.write_count = 0
    stats.done = 0

    for n in range(NWORKERS):
        goaway.goaway(worker, n)

    while stats.done < NWORKERS:
        time.sleep(.05)

    print "workers done", stats.done
    print "read count", stats.read_count
    if stats.read_count > 0:
        print "avg read time", stats.read_time / stats.read_count
    print "write count", stats.write_count
    if stats.write_count > 0:
        print "avg write time", stats.write_time / stats.write_count
