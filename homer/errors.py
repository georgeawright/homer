class MissingPerceptletError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class NoMoreCodelets(Exception):
    pass
