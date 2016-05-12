"""
Globals variables.

These are used by goaway methods invoked from application code
to get access to information that the goaway server has put here.
"""

import sys
import os
import uuid
import signal

# A config.ClusterConfig of the active config.
# Initialized by cmdserver.start_server.
# Initialized by RemoteControl.__init__.
config = None

# RemoteControl initialized by Goaway.__init__.
# Only populated on the spawner.
rc = None

# Server host (ip) as informed by being the spawner of a command line argument.
server_host = None

# Unique identifier for this process
# Initialized by ClusterConfig:__init__ on the spawner.
# Initialized by cmdserver:__main__ on remotes.
proc_uuid = uuid.uuid4()

# Datastore handles.
# Initialized by goaway:__init__ on the spawner.
# Initialized by cmdserver:__main__ on remotes.
# Map from kind -> datastore instance.
datastorehandles = {}
STRICT_CENTRALIZED = "strict"
LIN_FAST_READ = "lin_fast_read"
WEAK = "weak"
RELEASE = "release"
DATASTORE_TYPES = [STRICT_CENTRALIZED, WEAK, LIN_FAST_READ, RELEASE]

def get_data_store(kind):
    """Get a data store handle by its kind.
    Args:
        kind: The string name of the datastore kind.
    Raises an exception if the data stores have not yet been initialized.
    """
    if kind not in DATASTORE_TYPES:
        raise RuntimeError("Unrecognized datastore kind", kind)

    store = datastorehandles.get(kind)
    if store == None:
        raise RuntimeError("Datastore cannot be retrieved before initialization")
    return store

def init_data_stores():
    """Intialize all data stores.
    Requires that globalvars.config has already been set.
    """
    if config == None:
        raise RuntimeError("init_data_stores called before config set")
    if datastorehandles != {}:
        raise RuntimeError("attempt to re-initialize datastores")

    for kind in DATASTORE_TYPES:
        # These imports are down here to avoid circulatory problems. Unfortunate.
        if kind == STRICT_CENTRALIZED:
            from goaway.datastorehandle.strictcentralized import StrictCentralizedDataStoreHandle
            datastorehandles[kind] = StrictCentralizedDataStoreHandle()
        elif kind == WEAK:
            from goaway.datastorehandle.weak import WeakDataStoreHandle
            datastorehandles[kind] = WeakDataStoreHandle()
        elif kind == LIN_FAST_READ:
            from goaway.datastorehandle.linfastread import LinFastReadDataStoreHandle
            datastorehandles[kind] = LinFastReadDataStoreHandle()
        elif kind == RELEASE:
            from goaway.datastorehandle.updateonrelease import UpdateOnReleaseDataStoreHandle
            datastorehandles[kind] = UpdateOnReleaseDataStoreHandle()
        else:
            raise RuntimeError("unrecognized kind", kind)

def sigint(a, b):
    """ This runs when user kills the program.
        Original intention is to kill the remote servers
        When the user is finished using goaway """

    rc.kill_servers()
    sys.exit(0)
