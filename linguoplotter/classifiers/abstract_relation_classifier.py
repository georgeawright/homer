from linguoplotter.classifier import Classifier


class AbstractRelationClassifier(Classifier):
    def classify(self, **kwargs: dict):
        start = kwargs.get("start")
        end = kwargs.get("end")
        concept = kwargs.get("concept")

        return start.abstract_chunk.relations.filter(
            lambda x: x.parent_concept == concept
            and (
                (x.start == start.abstract_chunk and x.end == end.abstract_chunk)
                or (x.start == end.abstract_chunk and x.end == start.abstract_chunk)
            )
        ).not_empty
