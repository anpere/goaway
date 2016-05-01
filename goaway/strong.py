from consistency import ConsistencyModel
class Strong(ConsistencyModel):
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
        pass
    def __getattr_(self, name):
        pass
