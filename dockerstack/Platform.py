from abc import ABCMeta


class Platform(object):
    __metaclass__ = ABCMeta

    # Constructor
    def __init__(self):
        pass

    # Pre processing
    def pre_processing(self): raise NotImplementedError

    # Post processing scripts
    def post_processing(self): raise NotImplementedError
