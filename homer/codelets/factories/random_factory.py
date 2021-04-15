import random

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets import Factory
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Concept


class RandomFactory(Factory):
    """Spawns a random new codelet and a copy of itself"""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Factory.__init__(self, codelet_id, parent_id, bubble_chamber, coderack, urgency)

    def _engender_follow_up(self):
        action_type = self.bubble_chamber.spaces["activities"].contents.get_random()
        links_to_structure_nodes = StructureCollection(
            {
                link
                for link in action_type.links_out
                if link.end in self.bubble_chamber.spaces["structures"].contents
            }
        )
        structure_type = links_to_structure_nodes.get_random().end
        follow_up_type = self._get_follow_up_type(action_type, structure_type)
        proportion_of_follow_up_type_on_coderack = (
            self.coderack.number_of_codelets_of_type(follow_up_type) / 50
        )
        if proportion_of_follow_up_type_on_coderack < random.random():
            follow_up = follow_up_type.make(self.codelet_id, self.bubble_chamber)
            self.child_codelets.append(follow_up)
