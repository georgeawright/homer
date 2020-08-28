from abc import ABC, abstractmethod


class Classifier(ABC):
    @abstractmethod
    def confidence(self):
        pass
