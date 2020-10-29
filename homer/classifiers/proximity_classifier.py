from homer.classifier import Classifier


class ProximityClassifier(Classifier):
    from homer.structures import Chunk
    from homer.structures import Concept

    def __init__(self):
        pass

    def classify(self, concept: Concept, example: Chunk):
        return concept.proximity_to(example)
