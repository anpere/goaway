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
from config import ClusterConfig ## AP: imported so that main can create a config
import yaml
## AP: this will probably make somebody angry...
import dummyFile

import globalvars

app = Flask(__name__)

store = {}
store_lock = threading.RLock()


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"ok": "ok", "hello": "friend"})


@app.route("/check", methods=["GET"])
def check():
    """Check that a server is responding."""
    return jsonify({"ok": "ok"})

@app.route("/kill", methods=["POST"])
def kill():
    #TODO: implement kill_server()
    kill_server()
    return "killed server"

@app.route("/run", methods=["POST"])
def run():
    print "run recieved"
    call = request.json

    function_name = call["function_name"]
    function_args = call["args"]
    ## TODO: add function_module
    # function_module = call["function_module"]
    function_kwargs = call["kwargs"]
    ## TODO: check that dummyFile has function
    thread = threading.Thread(target=lambda: _run_in_thread(getattr(dummyFile, function_name), function_args, function_kwargs))
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
    time.sleep(2)
    print "running %s(%s)" %(function, args)
    result = function(*args, **kwargs)
    print "Server result {}".format(result)


def start_server(port, config):
    """Start the cmd server. This method is blocking.
    Args:
        port: Port to run on.
        config: Result of yaml.load'ing the config file.
    """
    globalvars.config = config
    debug = os.environ.get("DEBUG", False) == "true"
    print "Server debug", "on" if debug else "off"
    for module in config.data["modules"]:
        module_name, module_path = module.split(" ")
        module_path = os.path.expandvars(module_path)
        print module_name, module_path
        imp.load_source(module_name, module_path)
    try:
        # Always disable auto-reloader.
        # It is dangerous when running as a subprocess.
        app.run(host="0.0.0.0", port=port,
                debug=debug, use_reloader=False)
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


if __name__ == "__main__":
    assert len(sys.argv) == 2
    config_path = sys.argv[1]
    print "Configpath :%s" % (config_path)
    config_path = os.path.expandvars("$GOAWAYPATH/%s" % (config_path))
    with open(config_path, "r") as stream:
        config = ClusterConfig(yaml.load(stream))
    start_server(9060, config)
