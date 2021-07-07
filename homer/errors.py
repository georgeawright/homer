class MissingStructureError(Exception):
    def __init__(self, message=None):
        Exception.__init__(self, message)


class NoLocationError(Exception):
    def __init__(self, message=None):
        Exception.__init__(self, message)


class NoMoreCodelets(Exception):
    pass
