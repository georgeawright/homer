from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero


class Classifier:
    def classify(self, **kwargs: dict) -> FloatBetweenOneAndZero:
        raise NotImplementedError
