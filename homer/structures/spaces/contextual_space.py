import statistics

from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Concept


class ContextualSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        contents: StructureCollection,
        conceptual_spaces: StructureCollection = None,
    ):
        Space.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=contents,
            quality=0.0,
        )
        self.conceptual_spaces = (
            StructureCollection() if conceptual_spaces is None else conceptual_spaces
        )
        self.is_contextual_space = True

    @property
    def quality(self):
        active_contents = {
            structure for structure in self.contents if structure.activation > 0
        }
        if len(active_contents) == 0:
            return 0.0
        return statistics.fmean(
            [structure.quality * structure.activation for structure in active_contents]
        )

    def add(self, structure: Structure):
        if structure not in self.contents:
            self.contents.add(structure)

    def decay_activation(self, amount: float = None):
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        for item in self.contents:
            item.decay_activation(amount)

    def update_activation(self):
        self._activation = (
            statistics.median([item.activation for item in self.contents])
            if len(self.contents) != 0
            else 0.0
        )
