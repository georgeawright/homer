from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import ChunkSuggester
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation, corresponding_exigency
from homer.structures.views import MonitoringView


class ChunkProjectionSuggester(ChunkSuggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        ChunkSuggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_view = None
        self.target_word = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.chunk_builders import ChunkProjectionBuilder

        return ChunkProjectionBuilder

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
        target_view: MonitoringView = None,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = (
            bubble_chamber.monitoring_views.get(key=activation)
            if target_view is None
            else target_view
        )
        target_word = StructureCollection(
            {
                word
                for word in target_view.text_space.contents.where(is_word=True)
                if word.has_label(bubble_chamber.concepts["noun"])
            }
        ).get(key=corresponding_exigency)
        urgency = urgency if urgency is not None else target_word.uncorrespondedness
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"target_view": target_view, "target_word": target_word},
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    @property
    def target_structures(self):
        return StructureCollection({self.target_view, self.target_word})

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_word = self._target_structures["target_word"]
        return not self.target_word.has_correspondence_to_space(
            self.target_view.interpretation_space
        )

    def _calculate_confidence(self):
        self.confidence = 1.0

    def _fizzle(self):
        pass
