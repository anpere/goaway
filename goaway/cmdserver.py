#!/usr/bin/env python
"""Cmd server."""
server_debug = open("server.debug", 'w') ## TODO: handle multiple ports
def debug(message):
    server_debug.write(message+"\n")
    server_debug.flush()
from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
import inspect
import traceback
import os
import socket
import errno
import sys
import math
import time
import threading
import imp
import types
import uuid
import yaml

from config import ClusterConfig
from datatypes.lockingcontainer import LockingContainer
from goaway import globalvars ## AP: removed to temporarily fix problems with ^C
from goaway.datastorehandle.strictcentralized import StrictCentralizedDataStoreHandle
import goaway.objectconstructors as objectconstructors

app = Flask(__name__)

# TODO remove this
store_lock = threading.RLock()

locks_lock = threading.RLock() # hee hee hee
locks = {} # key: lock name (string); value: owner's uuid or None if unheld

# Keep track of which modules have been imported.
# (Container of) dict from module name to module if imported.
imported_modules_locked = LockingContainer({})


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"ok": "ok"})


@app.route("/check", methods=["GET"])
def check():
    """Check that a server is responding."""
    logging.debug("checked")
    return jsonify({"ok": "ok"})

@app.route("/kill", methods=["POST"])
def kill():
    app.logger.info("server killed")
    kill_server()
    return "killed server"

def kill_server():
    func = request.environ.get('werkzeug.server.shutdown')
    ok = "killed"
    if func is None:
        ok = "alive"
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return jsonify({"ok": ok})

@app.route("/run", methods=["POST"])
def run():
    call = request.json

    function_name = call["function_name"]
    function_args = call["args"]
    function_path = call["function_file"]
    function_kwargs = call["kwargs"]
    # app.logger.warning("file:%s"%(function_path))
    # app.logger.warning("file path:%s"% (os.getcwd()))
    module_name = inspect.getmodulename(function_path)
    # app.logger.warning(module_name)
    s_file = open(function_path, 'U')
    s_description = ('.py', 'U', 1)

    # Import the module or fetch it if already imported.
    with imported_modules_locked as imported_modules:
        if imported_modules.get(module_name):
            module = imported_modules[module_name]
        else:
            module = imp.load_module(module_name, s_file, function_path, s_description)
            imported_modules[module_name] = module

    ## TODO don't import modules that have already been imported
    ## if module_na not in getModules():
    ##     imp.load_source(module_name, function_path)
    function = getattr(module, function_name)
    app.logger.info("server starting: %s %s %s", function.__name__, function_args, function_kwargs)
    _run_in_thread(function, *function_args, **function_kwargs)
    return jsonify({"ok": "ok"})


@app.route("/data/create", methods=["POST"])
def data_create():
    """
    Initialize shared data in this server's local store.
    """
    consistency = request.json["consistency"]
    name = request.json["name"]

    if consistency=="strict":
        with store_lock:
            if name not in store:
                globalvars.strictCentralizedDataStoreHandle.create(name)
    elif consistency=="eventual":
        raise RuntimeError("EVENTUAL NOT IMPL")
        globalvars.eventualDataStoreHandle.create(name)



    res = {"ok": "ok"}
    return jsonify(res)


@app.route("/data/get", methods=["GET"])
def data_get():
    """
    Get shared data from this server's local store.
    """
    consistency = request.json["consistency"]
    name = request.json["name"]
    field = request.json["field"]
    value = ""
    error = "ok"
    if consistency == "strict":
        store = globalvars.get_data_store(globalvars.STRICT_CENTRALIZED_KIND)
        with store_lock:
            try:
                value = store.get(name, field)
            except AttributeError as ex:
                error = str(ex)
        res = {
            "value" : value,
            "error" : error,
        }

    return jsonify(res)


@app.route("/data/set", methods=["POST"])
def data_set():
    """
    Mutate shared data in this server's local store.
    """
    consistency = request.json["consistency"]
    name = request.json["name"]
    field = request.json["field"]
    value = request.json["value"]

    if consistency=="strict":
        store = globalvars.get_data_store(globalvars.STRICT_CENTRALIZED_KIND)
        with store_lock:
            store.set(name, field, value)
    res = {"ok": "ok"}
    return jsonify(res)

@app.route("/lock/acquire", methods=["POST"])
def acquire_lock():
    """ Attempt to acquire a shared lock. """
    requester_uuid = request.json['uuid']
    lock_name = request.json['name']
    with locks_lock:
        if lock_name in locks:
            if locks[lock_name] != None: # not reentrant
                res = {"ok": "false"}
                return jsonify(res)
        locks[lock_name] = requester_uuid
    app.logger.debug("lock [%s] acquired by [%s]", lock_name, requester_uuid)
    res = {"ok": "ok"}
    return jsonify(res)

@app.route("/lock/release", methods=["POST"])
def release_lock():
    """ Release a shared lock, if you are holding it. """
    requester_uuid = request.json['uuid']
    lock_name = request.json['name']
    with locks_lock:
        locks[lock_name] = None
        app.logger.debug("lock [%s] released", lock_name)
        res = {"ok": "ok"}
        return jsonify(res)
    res = {"ok": "false"}
    return jsonify(res)

def _run_in_thread(function, *args, **kwargs):
    """Run a function in a daemon thread."""
    thread = threading.Thread(target=function, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()

def setup_logging(port):
    """Configure logging for the server."""

    # Set up logging to only go to files.
    logfile = "server-{}.log".format(port)
    # handler = RotatingFileHandler(logfile, maxBytes=10000, backupCount=1)
    handler = logging.handlers.WatchedFileHandler(logfile)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger('')
    root_logger.addHandler(handler)

    # The following has been superceded by the root logger.
    # app.logger.handlers = []
    # app.logger.addHandler(handler)
    werkzeug_logger = logging.getLogger("werkzeug")
    # werkzeug_logger.handlers = []
    # werkzeug_logger.addHandler(handler)
    # # The werkzeug logger somehow still outputs to stdout, so this silences it.
    werkzeug_logger.setLevel(logging.ERROR)


def start_server(port, logging_has_been_setup=False):
    """Start the cmd server. This method is blocking.
    Args:
        port: Port to run on.
    """
    if not logging_has_been_setup:
        setup_logging(port)

    # Re-initialize the uuid, in case this was a fork.
    globalvars.proc_uuid = uuid.uuid4()
    debugOn = os.environ.get("DEBUG", False) == "true"

    ## TODO
    ##for module in config.data["modules"]:
    ##    module_name, module_path = module.split(" ")
    ##    module_path = os.path.expandvars(module_path)
    ##    imp.load_source(module_name, module_path)

    debug("start_server running")
    if debugOn:
        app.logger.warn("Server debug is on")

    try:
        # Always disable auto-reloader.
        # It is dangerous when running as a subprocess.
        app.run(host="0.0.0.0", port=port,
                debug=debugOn, use_reloader=False)
    except socket.error as exc:
        # Error when port in use.
        if exc.errno == errno.EADDRINUSE:
            print "Error: Could not start server on port {}. EADDRINUSE".format(port)
            sys.exit(-1)
        else:
            raise exc
    except KeyboardInterrupt:
        # Error when killed by user.
        print "Server exiting on port {} due to KeyboardInterrupt.".format(port)
        sys.exit(0)
    except Exception as ex:
        logging.exception(ex, exc_info=True)

## imported from http://stackoverflow.com/questions/4858100/how-to-list-imported-modules
def getModules():
    ''' Returns a list of the modules that have been  imported '''
    modules = []
    for name, val in globals().items():
        if isInstance(val, types.ModuleType):
            modules.append(val.__name__)


if __name__ == "__main__":
    # Show a separator.
    app.logger.info("Starting server..." + "\n" * 5 + "-" * 20 + "\n" * 5)

    # TODO this should be passed in on cmdline.
    port = 9060
    setup_logging(port)

    debug("main is running")
    logging.debug("main is running")
    assert len(sys.argv) == 2

    config_path = sys.argv[1]
    app.logger.debug("Configpath :%s" % (config_path))

    config = ClusterConfig(config_path)
    globalvars.config = config
    globalvars.init_data_stores()

    debug("starting server!")
    start_server(port, logging_has_been_setup=True)
