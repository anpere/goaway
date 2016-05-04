"""
Client for communicating with a cmdserver.
"""

import requests

from common import RpcException


class CmdClient(object):
    def __init__(self, user, host, port):
        self.user = user
        self.host = host
        self.port = port

    def check(self):
        """Check server health.
        Returns a boolean as to wether the server was reached.
        """
        try:
            res = requests.get(self._url("check"))
            resj = res.json()
            return resj["ok"]=="ok"
        except requests.exceptions.ConnectionError:
            return False
        except Exception as ex:
            # Actually, what kind of exceptions appear here?
            raise ex
        if res.status_code != 200:
            return False

    def kill(self):
        """Kills the mentioned server
        """
        print "posting:%s"%(self._url("kill"))
        try:
            res = requests.post(self._url("kill"))
            print "made kill"
            return True
        except Exception as ex:
            print ex
            return False
        if res.status_code != 200:
            print "not 200"
            return False

    def run_remote(self, file_name, function_name, *args, **kwargs):
        payload = {
            "function_name": function_name,
            "args": args,
            "kwargs" : kwargs,
            "function_file": file_name
        }
        print payload
        try:
            res = requests.post(self._url("run"), json=payload)
        except Exception as ex:
            raise RpcException("Could not connect to RPC server.", ex)
        if res.status_code != 200:
            raise RpcException("RPC server returned code {}".format(res.status_code), res.text)
        resj = res.json()
        if "error" in resj:
            raise RpcException(resj["error"])
        # return resj["return"]
        return

    def _url(self, path):
        return "http://{}:{}/{}".format(self.host, self.port, path)
