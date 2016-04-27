#!/usr/bin/env python
"""Cmd server."""
from flask import Flask, request, jsonify
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
from config import ClusterConfig ## AP: imported so that main can create a config
import yaml

import globalvars ## AP: removed to temporarily fix problems with ^C

app = Flask(__name__)

store = {}
store_lock = threading.RLock()
print "this runs all the time"
server_debug = open("server.debug", 'w') ## TODO: handle multiple ports

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"ok": "ok", "hello": "friend"})


@app.route("/check", methods=["GET"])
def check():
    app.logger.info("server was checked on")
    debug("server was checked on")
    """Check that a server is responding."""
    return jsonify({"ok": "ok"})

@app.route("/kill", methods=["POST"])
def kill():
    #TODO: implement kill_server()
    kill_server()
    return "killed server"

def kill_server():
    print "killed!!"
    func = request.environ.get('werkzeug.server.shutdown')
    ok = "killed"
    if func is None:
        ok = "alive"
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return jsonify({"ok": ok})

@app.route("/run", methods=["POST"])
def run():
    debug("run recieved")
    call = request.json
    print "run recieved"

    return
    function_name = call["function_name"]
    function_args = call["args"]
    function_path = call["function_file"]
    function_kwargs = call["kwargs"]
    module_name = inspect.getmodulename(function_path)
    module_file, module_pathname, module_description = imp.find_module(module_name)
    module = imp.load_module(module_name, module_file, module_pathname, module_description)
    '''
    todo: maybe not needed
    if module_na not in getModules():
        imp.load_source(module_name, function_path)
    print module
    '''
    print "server now running: %s(%s,%s)" % (getattr(module, function_name).__name__, function_args, function_kwargs)
    thread = threading.Thread(target=lambda: _run_in_thread(getattr(module, function_name), *function_args, **function_kwargs))
    thread.daemon = True
    thread.start()

    return jsonify({"ok": "ok"})


@app.route("/data/create", methods=["POST"])
def data_create():
    """
    Initialize shared data in this server's local store.
    """
    path = request.json["path"]
    default = request.json["default"]

    with store_lock:
        if path not in store:
            store[path] = default

    res = {"ok": "ok"}
    return jsonify(res)


@app.route("/data/get", methods=["GET"])
def data_get():
    """
    Get shared data from this server's local store.
    """
    path = request.json["path"]

    with store_lock:
        if path in store:
            res = {
                "value": store[path],
            }
        else:
            res = {
                "error": "NO_VAL_FOR_KEY",
            }

    return jsonify(res)


@app.route("/data/set", methods=["POST"])
def data_set():
    """
    Mutate shared data in this server's local store.
    """
    path = request.json["path"]
    value = request.json["value"]

    with store_lock:
        store[path] = value

    res = {"ok": "ok"}
    return jsonify(res)


def _run_in_thread(function, *args, **kwargs):
    # Simulate a slow execution.
    ## TODO: get rid of sleeps
    ## time.sleep(2)
    ## AP: had to get rid of time.sleep(2) because it wasn't working with it
    result = function(*args, **kwargs)
    print "Server result {}".format(result)


def start_server(port, config):
    """Start the cmd server. This method is blocking.
    Args:
        port: Port to run on.
        config: Result of yaml.load'ing the config file.
    """
    globalvars.config = config ## AP: removed to fix issues with ^C and many globalvars running sigint
    debugOn = os.environ.get("DEBUG", False) == "true"
    print "Server debug", "on" if debugOn else "off"
    debug("starting server")
    ''' TODO
    for module in config.data["modules"]:
        module_name, module_path = module.split(" ")
        module_path = os.path.expandvars(module_path)
        print module_name, module_path
        imp.load_source(module_name, module_path)
    '''
    try:
        # Always disable auto-reloader.
        # It is dangerous when running as a subprocess.
        handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
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
    print "HELLO"
    debug("main is running")
    assert len(sys.argv) == 2
    config_path = sys.argv[1]
    print "Configpath :%s" % (config_path)
    # config_path = os.path.expandvars("$GOAWAYPATH/%s" % (config_path))
    with open(config_path, "r") as stream:
        config = ClusterConfig(yaml.load(stream))
    start_server(9060, config)
