"""
Client for communicating with a cmdserver.
"""

import requests


class RpcException(Exception):
    """An exception that occurs because of an RPC call."""
    pass


class CmdClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def check(self):
        """Check server health.
        Returns a boolean as to weather the server was reached.
        """
        try:
            res = requests.get(self._url("check"))
            return True
        except Exception as ex:
            return False
        if res.status_code != 200:
            return False

    def run_remote(self, function_name, arg):
        payload = {
            "function_name": function_name,
            "arg": arg,
        }
        try:
            res = requests.post(self._url("run"), json=payload)
        except Exception as ex:
            raise RpcException("Could not connect to RPC server.", ex)
        if res.status_code != 200:
            raise RpcException("RPC server returned code {}".format(res.status_code))
        resj = res.json()
        if "error" in resj:
            raise RpcException(resj["error"])
        # return resj["return"]
        return

    def _url(self, path):
        return "http://{}:{}/{}".format(self.host, self.port, path)
