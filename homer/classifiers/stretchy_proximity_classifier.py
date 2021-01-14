from homer.classifier import Classifier


class StretchyProximityClassifier(Classifier):
    def __init__(self, proximity_weight: float = 0.6, neighbours_weight: float = 0.4):
        self.proximity_weight = proximity_weight
        self.neighbours_weight = neighbours_weight

    def classify(self, **kwargs: dict):
        concept = kwargs["concept"]
        start = kwargs["start"]
        proximity = concept.proximity_to(start)
        if len(start.neighbours) > 0:
            neighbours = start.neighbours.proportion_with_label(concept)
            return sum(
                [self.proximity_weight * proximity, self.neighbours_weight * neighbours]
            )
        return proximity
