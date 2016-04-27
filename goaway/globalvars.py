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
def sigint(a, b):
    print "Why you trying to globally kill me?"
    beforeKill = rc.check_servers()
    print "Servers Alive before kill?:%s" % (beforeKill)
    rc.kill_servers()
    afterKill = rc.check_servers()
    print "Servers Alive after kill?:%s" % (afterKill)
    ## Kill all the running servers
    sys.exit(0)
