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
print "rc set to None!!!"
rc = None
def sigint(a, b):
    ''' This runs when user kills the program.
        Original intention is to kill the remote servers
        When the user is finished using goaway '''

    print "Why you trying to globally kill me?"
    print "ref of rc in globalvars %s" % (rc.__hash__)
    beforeKill = rc.check_servers()
    print "Servers Alive before kill?:%s" % (beforeKill)
    rc.kill_servers()
    afterKill = rc.check_servers()
    print "Servers Alive after kill?:%s" % (afterKill)
    sys.exit(0)
