from linguoplotter.classifier import Classifier
from linguoplotter.errors import MissingStructureError


class LastWordOfTypeClassifier(Classifier):
    def classify(self, **kwargs: dict):
        start = kwargs.get("start")
        space = kwargs["space"]

        previous = start
        while True:
            try:
                previous = start.right_neighbour
                if previous.has_location_in_space(space):
                    return 0.0
            except MissingStructureError:
                return 1.0
