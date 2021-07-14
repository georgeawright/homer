from homer.float_between_one_and_zero import FloatBetweenOneAndZero


class Classifier:
    def classify_link(self, **kwargs: dict) -> FloatBetweenOneAndZero:
        raise NotImplementedError

    def classify_chunk(self, **kwargs: dict) -> FloatBetweenOneAndZero:
        raise NotImplementedError
