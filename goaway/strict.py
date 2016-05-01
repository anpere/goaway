from objecthandler import ObjectHandler
class Strict(ObjectHandler):
    """
    Represents shared memory with weak consistencies
    On creation this data is shared with other machines
    Clients can set fields in this object and use them as
    they want.
    For example:
        zoobar = Weak()
        zoobars.clients = {}
        zoobars.clients["alyssa"] = 10

    """
    def __init__(self):
        pass
    def __setattr__(self, name, value):
        print "name:%s value%s"% (name, value)
    def __getattr__(self, name):
        print "name:%s "% (name)
