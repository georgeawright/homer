from typing import Any, List

from homer.classifier import Classifier
from homer.float_between_zero_and_one import FloatBetweenZeroAndOne
from homer.structures.chunk import Chunk
from homer.structures.link import Link
from homer.structures.space import Space


class Concept(Structure):
    def __init__(
        self,
        name: str,
        prototype: Any,
        classifier: Classifier,
        parent_space: Space,
        child_spaces: List[Space],
        links_in: List[Link] = None,
        links_out: List[Link] = None,
        depth: int = 1,
        activation: FloatBetweenZeroAndOne = FloatBetweenZeroAndOne(0),
    ):
        location = None
        links_in = [] if links_in is None else links_in
        links_out = [] if links_out is None else links_out
        Structure.__init__(self, location, links_in, links_out)
        self.name = name
        self.prototype = prototype
        self.classifier = classifier
        self.parent_space = parent_space
        self.child_spaces = spaces
        self.depth = depth
        self.activation = activation

    def classify_example(self, example: Structure) -> FloatBetweenZeroAndOne:
        return self.classifier.classify(example)
