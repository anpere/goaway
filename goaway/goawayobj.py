class GoawayObject(object):
    """ Users can inherit from this class to create their own
        goaway compatible mutable objects.
        Users can overwrite __setattr__ and getattr__ at their own risk
    """

    def __init__(self):
        pass

   def __getattr__(self, field):
       pass

   def __setattr__(self, field, value):
       pass
