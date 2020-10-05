class MissingPerceptletError(Exception):
    def __init__(self, message=None):
        Exception.__init__(self, message)


class FailedGettingRequirements(Exception):
    pass


class NoMoreCodelets(Exception):
    pass
