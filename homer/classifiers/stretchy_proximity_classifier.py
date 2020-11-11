from homer.classifier import Classifier


class StretchyProximityClassifier(Classifier):
    def __init__(self, proximity_weight: float = 0.6, neighbours_weight: float = 0.4):
        self.proximity_weight = proximity_weight
        self.neighbours_weight = neighbours_weight

    def classify(self, arguments: dict):
        proximity = arguments["concept"].proximity_to(arguments["start"])
        if len(arguments["start"].neighbours) > 0:
            neighbours = arguments["start"].neighbours.proportion_with_label(
                arguments["concept"]
            )
            return sum(
                [self.proximity_weight * proximity, self.neighbours_weight * neighbours]
            )
        return proximity
