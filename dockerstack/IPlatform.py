class IPlatform:

    # Pre processing
    def __init__(self):
        pass

    def pre_processing(self): raise NotImplementedError

    # Post processing script
    def post_processing(self): raise NotImplementedError
