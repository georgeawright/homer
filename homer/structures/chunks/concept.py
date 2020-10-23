from typing import Any, List

from homer.classifier import Classifier
from homer.structures.chunks import Chunk
from homer.structures.links import Link


class Concept(Chunk):
    def __init__(
        self,
        prototype: Any,
        classifier: Classifier,
        links_in: List[Link] = None,
        links_out: List[Link] = None,
    ):
        value = None
        location = None
        members = []
        neighbours = []
        links_in = [] if links_in is None else links_in
        links_out = [] if links_out is None else links_out
        Chunk.__init__(self, value, location, members, neighbours, links_in, links_out)
        self.prototype = prototype
        self.classifier = classifier
