class Weak(object):
    """
    Represents shared memory with weak consistencies

    Clients can set fields in this object and use them as
    they want.
    For example:
        zoobar = WEAK()
        zoobars.clients = {}
        zoobars.clients["alyssa"] = 10

    """
