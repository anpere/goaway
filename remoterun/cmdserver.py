"""Cmd server."""
from flask import Flask, request, jsonify
import os
import inspect
import traceback
import socket
import errno
import sys
import math


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

    dummy_functions = {
        "square": lambda x: x * x,
        "cube": lambda x: x * x * x,
        "sqrt": lambda x: math.sqrt(x),
    }

    if not function_name in dummy_functions:
        return jsonify({"error": "no such function"})

    result = dummy_functions[function_name](function_arg)
    return jsonify({"return": result})


def start_server(port):
    """Start the cmd server. This method is blocking."""
    debug = os.environ.get("DEBUG", False) == "true"
    print "Server debug", "on" if debug else "off"
    try:
        app.run(host="0.0.0.0", port=port, debug=debug)
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
