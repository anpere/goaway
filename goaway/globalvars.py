"""
Globals variables.

These are used by goaway methods invoked from application code
to get access to information that the goaway server has put here.
"""

# A config.ClusterConfig of the active config.
# Initialized by cmdserver.start_server.
# Initialized by RemoteControl.__init__.
config = None
