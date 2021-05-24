from __future__ import annotations

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Chunk


class ChunkSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_one = None
        self.target_two = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders import ChunkBuilder

        return ChunkBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target = bubble_chamber.input_nodes.where(is_chunk=True).get_unhappy()
        urgency = urgency if urgency is not None else target.unhappiness
        return cls.spawn(parent_id, bubble_chamber, {"target_one": target}, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        self.target_one = self._target_structures["target_one"]
        try:
            self.target_two = self.target_one.nearby().get_random()
            self._target_structures["target_two"] = self.target_two
        except MissingStructureError:
            return False
        return not self.bubble_chamber.has_chunk(
            StructureCollection.union(
                self._members_from_chunk(self.target_one),
                self._members_from_chunk(self.target_two),
            )
        )

    def _calculate_confidence(self):
        distances = [
            space.proximity_between(self.target_one, self.target_two)
            for space in self.target_one.parent_spaces
            if space.is_basic_level
        ]
        self.confidence = 0.0 if distances == [] else fuzzy.AND(*distances)

    def _fizzle(self):
        pass

    def _members_from_chunk(self, chunk):
        return StructureCollection({chunk}) if chunk.size == 1 else chunk.members
