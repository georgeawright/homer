from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.classifiers import SamenessClassifier
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structure_collection_keys import chunking_exigency


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
        self.target_structure_one = target_structures.get("target_structure_one")
        self.target_structure_two = target_structures.get("target_structure_two")

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import ChunkBuilder

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
        target_space = bubble_chamber.input_spaces.get()
        target_node = target_space.contents.where(is_node=True).get(
            key=chunking_exigency
        )
        urgency = urgency if urgency is not None else target_node.unchunkedness
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_structure_one": target_node,
            },
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        return cls.make(parent_id, bubble_chamber, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    @property
    def targets_dict(self):
        return {
            "target_structure_one": self.target_structure_one,
            "target_structure_two": self.target_structure_two,
        }

    def _passes_preliminary_checks(self) -> bool:
        try:
            if self.target_structure_two is None:
                self.target_structure_two = (
                    self.target_structure_one.potential_chunk_mates.get(
                        key=chunking_exigency
                    )
                )
            return True
        except MissingStructureError:
            return False

    def _calculate_confidence(self):
        collection_one = (
            self.bubble_chamber.new_structure_collection(self.target_structure_one)
            if self.target_structure_one.members.is_empty()
            else self.target_structure_one.members
        )
        collection_two = (
            self.bubble_chamber.new_structure_collection(self.target_structure_two)
            if self.target_structure_two.members.is_empty()
            else self.target_structure_two.members
        )
        self.confidence = SamenessClassifier().classify(
            collection=StructureCollection.union(collection_one, collection_two),
            concept=self.bubble_chamber.concepts["same"],
        )

    def _fizzle(self):
        pass
