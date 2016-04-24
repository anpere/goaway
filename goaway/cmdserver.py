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


@app.route("/run", methods=["POST"])
def run():
    call = request.json

    function_name = call["function_name"]
    function_arg = call["arg"]

    ## TODO: check that dummyFile has function
    thread = threading.Thread(target=lambda: _run_in_thread(getattr(dummyFile, function_name), function_arg))
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


def _run_in_thread(function, arg):
    # Simulate a slow execution.
    ## TODO: get rid of sleeps
    time.sleep(2)
    result = function(arg)
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
    module_name, module_path = config.data["modules"].split(" ")
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
    start_server(port=9060)
