class ConsistencyModel(object):
    """ Represents a group of data whose accesses across different
        machines satisfies a consistency model.
        Objects of different consistencies models all inherit from ConsistencyModel,
        and ConsistencyModel may be used to define operations they all share in common
    """
    def __setattr__(self, name, value):
        pass
    def __getattr__(self, name):
        pass
