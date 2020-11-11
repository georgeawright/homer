from homer.classifier import Classifier


class StretchyProximityClassifier(Classifier):
    from homer.structures import Chunk
    from homer.structures import Concept

    def __init__(self, proximity_weight: float = 0.6, neighbours_weight: float = 0.4):
        self.proximity_weight = proximity_weight
        self.neighbours_weight = neighbours_weight

    def classify(self, concept: Concept, example: Chunk):
        proximity = concept.proximity_to(example)
        if len(example.neighbours) > 0:
            neighbours = example.neighbours.proportion_with_label(concept)
            return sum(
                [self.proximity_weight * proximity, self.neighbours_weight * neighbours]
            )
        return proximity
