#!/usr/bin/env python
"""Cmd server."""
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
from config import ClusterConfig ## AP: imported so that main can create a config
import yaml
from datatypes.lockingcontainer import LockingContainer

import globalvars ## AP: removed to temporarily fix problems with ^C
from strictcentralizeddatastorehandle import StrictCentralizedDataStoreHandle
import objectconstructors

app = Flask(__name__)

# Storage for StrictCentralizedDatastore
# TODO rename this.
store = {}
store_lock = threading.RLock()

locks_lock = threading.RLock() # hee hee hee
locks = {} # key: lock name (string); value: owner's uuid or None if unheld

# Keep track of which modules have been imported.
# (Container of) dict from module name to module if imported.
imported_modules_locked = LockingContainer({})

server_debug = open("server.debug", 'w') ## TODO: handle multiple ports

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"ok": "ok", "hello": "friend, 8"})


@app.route("/check", methods=["GET"])
def check():
    """Check that a server is responding."""
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
                store[name] = objectconstructors.StrictCentralized(name)

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
    value = "NONE"
    error = "ok"
    if consistency=="strict":
        with store_lock:
            if name in store:
                try:
                    value = store[name]
                except KeyError:
                    app.logger.warning("Key error for name: %s , field: %s" % (name, field))
                    error = "Object<{}> has no such attribute '{}'".format(object_name, key)
            else:
                    error = "NO_VAL_FOR_KEY"

    res = { "value" : value,
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
        with store_lock:
            if name not in store:
                app.logger.warning("%s not in store, putting" % (name))
                store[name] = {}
            app.logger.info("setting %s.%s to %s" % (name, field, value))
            store[name][field] = value

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
    root_logger.handlers = []
    root_logger.addHandler(handler)

    # The following has been superceded by the root logger.
    # app.logger.handlers = []
    # app.logger.addHandler(handler)
    werkzeug_logger = logging.getLogger("werkzeug")
    # werkzeug_logger.handlers = []
    # werkzeug_logger.addHandler(handler)
    # # The werkzeug logger somehow still outputs to stdout, so this silences it.
    werkzeug_logger.setLevel(logging.ERROR)


def start_server(port, config):
    """Start the cmd server. This method is blocking.
    Args:
        port: Port to run on.
        config: Result of yaml.load'ing the config file.
    """
    # Re-initialize the uuid, in case this was a fork.
    globalvars.proc_uuid = uuid.uuid4()
    globalvars.config = config ## AP: removed to fix issues with ^C and many globalvars running sigint
    debugOn = os.environ.get("DEBUG", False) == "true"

    setup_logging(port)

    ## TODO
    ##for module in config.data["modules"]:
    ##    module_name, module_path = module.split(" ")
    ##    module_path = os.path.expandvars(module_path)
    ##    imp.load_source(module_name, module_path)

    debug("start_server running")
    # Show a separator.
    app.logger.info("Starting server..." + "\n" * 5 + "-" * 20 + "\n" * 5)
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

def debug(message):
    server_debug.write(message+"\n")
    server_debug.flush()
if __name__ == "__main__":
    debug("main is running")
    app.logger.debug("main is running")
    assert len(sys.argv) == 2
    config_path = sys.argv[1]
    app.logger.debug("Configpath :%s" % (config_path))
    ## create datastores
    globalvars.strictCentralizedDataStoreHandle = StrictCentralizedDataStoreHandle()
    # config_path = os.path.expandvars("$GOAWAYPATH/%s" % (config_path))
    debug("strict data store made")
    with open(config_path, "r") as stream:
        config = ClusterConfig(yaml.load(stream))
    start_server(9060, config)
