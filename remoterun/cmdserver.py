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

app = Flask(__name__)


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

def _run_in_thread(function, arg):
    # Simulate a slow execution.
    ## TODO: get rid of sleeps
    time.sleep(2)
    result = function(arg)
    print "Server result {}".format(result)


def start_server(port):
    """Start the cmd server. This method is blocking."""
    debug = os.environ.get("DEBUG", False) == "true"
    print "Server debug", "on" if debug else "off"
    try:
        # Always disable auto-reloader.
        # It is dangerous when running as a subprocess.
        app.run(host="0.0.0.0", port=port,
                debug=debug, use_reloader=False)
    except socket.error as exc:
        if exc.errno == errno.EADDRINUSE:
            print "Error: Could not start server on port {}. EADDRINUSE".format(port)
            sys.exit(-1)
        else:
            raise exc
    except KeyboardInterrupt:
        print "Server exiting on port {} due to KeyboardInterrupt.".format(port)
        sys.exit(0)


if __name__ == "__main__":
    start_server(port=9060)
