from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.classifiers import SamenessClassifier
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict, StructureSet
from linguoplotter.structure_collection_keys import chunking_exigency


class ChunkSuggester(Suggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import ChunkBuilder

        return ChunkBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        space = bubble_chamber.input_spaces.get()
        node_one = space.contents.where(is_node=True).get(
            key=lambda x: x.unchunkedness * (len(x.potential_chunk_mates) > 0)
        )
        urgency = (
            urgency
            if urgency is not None
            else node_one.unchunkedness * (len(node_one.potential_chunk_mates) > 0)
        )
        targets = bubble_chamber.new_dict({"node_one": node_one}, name="targets")
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

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

    def _passes_preliminary_checks(self) -> bool:
        if self.targets["members"] is None:
            if self.targets["node_two"] is None:
                try:
                    self.targets["node_two"] = self.targets[
                        "node_one"
                    ].potential_chunk_mates.get(key=chunking_exigency)
                except MissingStructureError:
                    return False
            self.targets["members"] = StructureSet.union(
                self.targets["node_one"].raw_members,
                self.targets["node_two"].raw_members,
            )
        return True

    def _calculate_confidence(self):
        self.confidence = SamenessClassifier().classify(
            collection=self.targets["members"],
            concept=self.bubble_chamber.concepts["same"],
            spaces=self.targets["node_one"].parent_spaces.filter(
                lambda x: x.is_conceptual_space
                and x.is_basic_level
                and x.name != "size"
            ),
        )

    def _fizzle(self):
        pass
