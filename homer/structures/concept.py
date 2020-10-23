from typing import Any, List

from homer.classifier import Classifier
from homer.structure import Structure


class Concept(Structure):
    def __init__(
        self,
        prototype: Any,
        classifier: Classifier,
        links_in: List[Structure],
        links_out: List[Structure],
    ):
        Structure.__init__(self, None, links_in, links_out)
        self.prototype = prototype
        self.classifier = classifier
