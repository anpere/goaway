"""
Common functionality in examples.
"""

import sys
import os

def select_config():
    """Select a config file to use.
    Args:
        sys.argv is read.
    Returns:
        abspath to the config file.
    """
    error_message = "expected locality argument to be either all, remote, or local"
    if len(sys.argv) < 2:
        sys.exit(error_message)
    place = sys.argv[1]
    if place =="remote":
        config_name = "remote.yaml"
    elif place =="local":
        config_name = "local.yaml"
    elif place =="all":
        config_name = "config.yaml"
    else:
        sys.exit(error_message)
    config_path = os.path.join(os.path.dirname(__file__), config_name)
    return config_path
