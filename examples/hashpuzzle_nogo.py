"""
The same as hashpuzzle.py, but without using GoAway and using local processes instead.
"""

import os
import math
import time
import hashlib
import multiprocessing

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

    # Split the nonce space into workers different sections.
    # bounds is a list of tuples of (min, max) values for chunks.
    bounds = split_range(nonce_min, nonce_max, nworkers)
    assert len(bounds) == nworkers

    # Run a thread for each range.
    pool = multiprocessing.Pool(nworkers)
    argses = [(seed, a, b) for (a, b) in bounds]
    retvals = pool.map(worker, argses)

    results = [x for x in retvals if x != None]

    if results:
        return results[0]
    else:
        return None

def worker(args):
    return run_chunk(*args)

def run_chunk(seed, nonce_min, nonce_max):
    """
    Works on a chunk of the nonce space.
    """
    for nonce in xrange(nonce_min, nonce_max+1):
        candidate = seed + str(nonce)
        hashed = sha512(candidate)
        if constraint(hashed):
            return candidate
    return None

if __name__ == "__main__":
    start_time = time.time()
    result_solution = solve_puzzle(
        nworkers=20,
        seed="prefix-",
        nonce_min=0,
        nonce_max=30000000,
    )
    end_time = time.time()
    print "solve_puzzle took {} seconds".format(end_time - start_time)

    if result_solution:
        print "solution", result_solution
        print "hash", sha512(result_solution)[:15], "..."
        print "check", constraint(sha512(result_solution))
    else:
        print "No solution found."
