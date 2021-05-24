import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import LabelSuggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Label
from homer.structures.nodes import Chunk, Word
from homer.structures.views import MonitoringView


class LabelProjectionSuggester(LabelSuggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        LabelSuggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_view = None
        self.target_chunk = None
        self.target_word = None
        self.parent_concept = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.label_builders import LabelProjectionBuilder

        return LabelProjectionBuilder

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
            bubble_chamber.monitoring_views.get_active()
            if target_view is None
            else target_view
        )
        target_chunk = target_view.interpretation_space.contents.where(
            is_chunk=True
        ).get_unhappy()
        potential_labeling_words = (
            target_chunk.correspondences_to_space(target_view.text_space)
            .get_random()
            .arguments.get_random(exclude=[target_chunk])
            .potential_labeling_words
        )
        target_word = StructureCollection(
            {
                word
                for word in potential_labeling_words
                if all(
                    not isinstance(
                        correspondence.arguments.get_random(exclude=[word]), Label
                    )
                    for correspondence in word.correspondences_to_space(
                        target_view.interpretation_space
                    )
                )
            }
        ).get_unhappy()
        urgency = (
            urgency
            if urgency is not None
            else statistics.fmean([target_chunk.unlinkedness, target_word.unlinkedness])
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_chunk": target_chunk,
                "target_word": target_word,
            },
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    @property
    def target_structures(self):
        return StructureCollection(
            {self.target_view, self.target_word, self.target_chunk}
        )

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_word = self._target_structures["target_word"]
        self.target_chunk = self._target_structures["target_chunk"]
        try:
            self.parent_concept = self.target_word.lexeme.concepts.get_random()
            self._target_structures["parent_concept"] = self.parent_concept
        except MissingStructureError:
            return False
        return not self.target_chunk.has_label(self.parent_concept) and all(
            not isinstance(
                correspondence.arguments.get_random(exclude=[self.target_word]), Label
            )
            for correspondence in self.target_word.correspondences_to_space(
                self.target_view.interpretation_space
            )
        )

    def _calculate_confidence(self):
        self.confidence = FloatBetweenOneAndZero(
            self.parent_concept.parent_space
            in self.bubble_chamber.spaces["label concepts"].contents
        )
