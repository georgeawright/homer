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
        self.target_members = None

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
            key=lambda x: x.unchunkedness * (len(x.potential_chunk_mates) > 0)
        )
        urgency = (
            urgency
            if urgency is not None
            else target_node.unchunkedness
            * (len(target_node.potential_chunk_mates) > 0)
        )
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
            "target_members": self.target_members,
        }

    def _passes_preliminary_checks(self) -> bool:
        if self.target_members is None:
            if self.target_structure_two is None:
                try:
                    self.target_structure_two = (
                        self.target_structure_one.potential_chunk_mates.get(
                            key=chunking_exigency
                        )
                    )
                except MissingStructureError:
                    return False
            self.target_members = StructureCollection.union(
                self.target_structure_one.raw_members,
                self.target_structure_two.raw_members,
            )
            self.bubble_chamber.loggers["activity"].log_collection(
                self, self.target_members, "Target members"
            )
        return True

    def _calculate_confidence(self):
        self.confidence = SamenessClassifier().classify(
            collection=self.target_members,
            concept=self.bubble_chamber.concepts["same"],
            spaces=self.target_structure_one.parent_spaces.filter(
                lambda x: x.is_conceptual_space
                and x.is_basic_level
                and x.name != "size"
            ),
        )

    def _fizzle(self):
        pass
