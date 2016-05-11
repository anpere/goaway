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
rc = None

# Unique identifier for this process
proc_uuid = uuid.uuid4()

# Datastore handles.
# Initialized by goaway:__init__ on the spawner.
# Initialized by cmdserver:__main__ on remotes.
# Map from kind -> datastore instance.
datastorehandles = {}
STRICT_CENTRALIZED_KIND= "strict_centralized"
WEAK_KIND = "weak_kind"
ALL_KINDS = [STRICT_CENTRALIZED_KIND, WEAK_KIND]

def get_data_store(kind):
    """Get a data store handle by its kind.
    Args:
        kind: The string name of the datastore kind.
    Raises an exception if the data stores have not yet been initialized.
    """
    if kind not in ALL_KINDS:
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

    for kind in ALL_KINDS:
        # These imports are down here to avoid circulatory problems. Unfortunate.
        if kind == STRICT_CENTRALIZED_KIND:
            from goaway.datastorehandle.strictcentralized import StrictCentralizedDataStoreHandle
            datastorehandles[STRICT_CENTRALIZED_KIND] = StrictCentralizedDataStoreHandle()
        elif kind == WEAK_KIND:
            from goaway.datastorehandle.weak import WeakDataStoreHandle
            datastorehandles[WEAK_KIND] = WeakDataStoreHandle()
        else:
            raise RuntimeError("unrecognized kind", kind)


## TODO AP: miles thinks this is sketchy, remove it eventually
def sigint(a, b):
    """ This runs when user kills the program.
        Original intention is to kill the remote servers
        When the user is finished using goaway """

    rc.kill_servers()
    sys.exit(0)
