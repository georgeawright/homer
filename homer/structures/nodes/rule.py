from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node

from .concept import Concept


class Rule(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        location: Location,
        root: Concept,
        left_branch: Concept,
        right_branch: Concept,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        stable_activation: FloatBetweenOneAndZero = None,
    ):
        quality = None
        Node.__init__(
            self,
            structure_id,
            parent_id,
            value=location.coordinates,
            locations=[location],
            parent_space=location.space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            stable_activation=stable_activation,
        )
        self.name = name
        self._value = name
        self.root = root
        self.left_branch = left_branch
        self.right_branch = right_branch
