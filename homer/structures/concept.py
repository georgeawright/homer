from typing import Any, List

from homer.classifier import Classifier
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection import StructureCollection

from .chunk import Chunk
from .link import Link
from .space import Space


class Concept(Structure):
    def __init__(
        self,
        name: str,
        prototype: Any,
        classifier: Classifier,
        parent_space: Space,
        child_spaces: StructureCollection,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        depth: int = 1,
        activation: FloatBetweenOneAndZero = FloatBetweenOneAndZero(0),
    ):
        location = None
        Structure.__init__(self, location, links_in, links_out)
        self.name = name
        self.prototype = prototype
        self.classifier = classifier
        self.parent_space = parent_space
        self.child_spaces = child_spaces
        self.depth = depth
        self.activation = activation

    def classify_example(self, example: Structure) -> FloatBetweenOneAndZero:
        return self.classifier.classify(self, example)
