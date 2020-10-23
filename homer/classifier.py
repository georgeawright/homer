from abc import ABC, abstractmethod


class Classifier(ABC):
    @abstractmethod
    # possibly rename to goodness-of-example
    def confidence(self):
        pass
