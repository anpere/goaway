import requests

import globalvars
from common import RpcException

def rpc(http_method, url, payload):
    """Issue an rpc.
    Raises if "error" is a key in the response.
    Returns the json response.
    Args:
        http_method: One of "GET" or "POST".
        url: Url to send the request to.
        payload: Payload to send with request.
    """
    if globalvars.config == None:
        raise RuntimeError("globalvars.config not yet initialized.")
    try:
        if http_method == "GET":
            res = requests.get(url, json=payload)
        elif http_method == "POST":
            res = requests.post(url, json=payload)
        else:
            raise RuntimeError("Unsupported HTTP type {}".format(http_method))
    except requests.exceptions.RequestException as ex:
        # TODO retry
        # TODO catch a less broad exception.
        raise RpcException("Could not connect to RPC server.", ex)
    if res.status_code != 200:
        # save_error_html(res.text)
        raise RpcException("RPC server returned code {}".format(res.status_code))
    resj = res.json()
    if "error" in resj:
        if resj["error"] != "ok":
            raise RpcException(resj["error"])
    return resj

def master_url(url_subpath):
    """Create a URL for contacting the data master."""
    # The data master is the first server listed in the config.
    master_server = globalvars.config.servers[0]
    return "http://{}:{}/{}".format(master_server.host, master_server.port, url_subpath)

def save_error_html(html):
    """Hacky debugging thing."""
    LAST_ERROR_PATH = "./error.html"
    os.unlink(LAST_ERROR_PATH)
    with open(LAST_ERROR_PATH, "w") as f:
        f.write(res.text)
