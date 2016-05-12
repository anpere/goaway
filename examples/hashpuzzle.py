"""
Example program that solves a hash puzzle.
The puzzle is like that of mining a bitcoin block.

For a given seed string, find a number such that when that number is
appended to the seed and the result is hashed, it satisfies some
constraint. An example constraint could be that the result starts
with some number of consecutive 0's.
In other words, find an x such that constraint(hash(seed + x)) is true.

The program optionally uses GoAway. So that you can see the speed
difference when running locally vs distributed across many machines.
"""

import os
import math
import time
import hashlib

import goaway

worker_stats_lock = goaway.Lock("worker_stats_lock")
worker_stats = goaway.LinFastRead("worker_stats")
result = goaway.StrictCentralized("result")

def constraint(x):
    """Decide whether the problem is solved. (string -> bool)."""
    difficulty = 6
    return x[:difficulty] == "0" * difficulty

def sha512(x):
    """Hash function. (string -> string)"""
    return hashlib.sha512(x).hexdigest()

def split_range(vmin, vmax, nchunks):
    """Splits a range of numbers into chunks.
    Args:
        vmin, vmax: min and max values in the range.
        nchunks: number of chunks to split it into.
    Returns: A list of nchunks bounds pairs (min, max).
             val[0][0] == nonce_min
             val[-1][1] == nonce_max
    """
    assert nchunks > 0
    assert nchunks <= (vmax - vmin)
    step = (vmax - vmin) / float(nchunks)
    bounds = []
    for ci in xrange(nchunks):
        a = vmin + ci * step
        b = a + step
        bounds.append((int(a), int(b)))
    assert bounds[0][0] == vmin
    assert bounds[-1][1] == vmax
    assert len(bounds) == nchunks, (len(bounds), nchunks)
    return bounds

def solve_puzzle(nworkers, seed, nonce_min, nonce_max):
    """
    Solve a hash puzzle.
    Args:
        nworkers: How many workers to work on the task.
        seed: Prefix of the hashed value.
        nonce_min: Minimum value to append to the seed.
        nonce_max: Maximum value to append to the seed.
    Returns: (seed, nonce)
        The seed and nonce that yield and accepted result.
    """
    print "seed: {}, range {} -> {}".format(seed, nonce_min, nonce_max)
    print "Working on puzzle with {} workers.".format(nworkers)

    worker_stats.done = 0
    result.solution = None

    # Split the nonce space into workers different sections.
    # bounds is a list of tuples of (min, max) values for chunks.
    bounds = split_range(nonce_min, nonce_max, nworkers)
    assert len(bounds) == nworkers

    # Run a thread for each range.
    for a, b in bounds:
        goaway.goaway(run_chunk, seed, a, b)

    while worker_stats.done < nworkers:
        time.sleep(.05)

    return result.solution

def run_chunk(seed, nonce_min, nonce_max):
    """
    Works on a chunk of the nonce space.
    """
    for nonce in xrange(nonce_min, nonce_max+1):
        candidate = seed + str(nonce)
        hashed = sha512(candidate)
        if constraint(hashed):
            result.solution = candidate
            break

    with worker_stats_lock:
        worker_stats.done += 1

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), 'remote.yaml')

    goaway.init(config_path)

    start_time = time.time()
    solve_puzzle(
        nworkers=20,
        seed="prefix-",
        nonce_min=0,
        nonce_max=30000000,
    )
    end_time = time.time()
    print "solve_puzzle took {} seconds".format(end_time - start_time)

    if result.solution:
        print "solution", result.solution
        print "hash", sha512(result.solution)[:15], "..."
        print "check", constraint(sha512(result.solution))
    else:
        print "No solution found."
