"""
Configure logging.
"""

import logging
import sys

def setup():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s")

    # Silence requests logging.
    logging.getLogger("requests").setLevel(logging.WARNING)

    stream = logging.StreamHandler(sys.stdout)
    stream.setLevel(logging.INFO)
    stream.setFormatter(formatter)

    root.addHandler(stream)
