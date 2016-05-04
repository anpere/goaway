import signal
import sys

"""
Globals variables.

These are used by goaway methods invoked from application code
to get access to information that the goaway server has put here.
"""
# A config.ClusterConfig of the active config.
# Initialized by cmdserver.start_server.
# Initialized by RemoteControl.__init__.
config = None

# RC initialized by Goaway.__init__.

rc = None
strictCentralizedDataStoreHandle = None
weakDataStoreHandle = None

## TODO AP: miles thinks this is sketchy, remove it eventually
def sigint(a, b):
    """ This runs when user kills the program.
        Original intention is to kill the remote servers
        When the user is finished using goaway """

    rc.kill_servers()
    sys.exit(0)
