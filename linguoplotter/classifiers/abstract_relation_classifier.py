from linguoplotter.classifier import Classifier


class AbstractRelationClassifier(Classifier):
    def classify(self, **kwargs: dict):
        start = kwargs.get("start")
        end = kwargs.get("end")
        concept = kwargs.get("concept")

        if start.abstract_chunk.relations.filter(
            lambda x: x.end == end.abstract_chunk and x.parent_concept == concept
        ).not_empty:
            return 1.0
        return 0.0
