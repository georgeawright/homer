import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import RelationSuggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Chunk, Concept
from homer.structures.views import MonitoringView


class RelationProjectionSuggester(RelationSuggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        RelationSuggester.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )
        self.target_view = None
        self.target_structure_two = None
        self.target_structure_two = None
        self.target_word = None
        self.parent_concept = None
        self.conceptual_space = None
        self.child_structure = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.relation_builders import RelationProjectionBuilder

        return RelationProjectionBuilder

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
        target_chunk = target_view.interpretation_space.contents.of_type(
            Chunk
        ).get_unhappy()
        potential_relating_words = (
            target_chunk.correspondences_to_space(target_view.text_space)
            .get_random()
            .arguments.get_random(exclude=[target_chunk])
            .potential_relating_words
        )
        target_word = StructureCollection(
            {
                word
                for word in potential_relating_words
                if not word.has_correspondence_to_space(
                    target_view.interpretation_space
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
                "target_structure_one": target_chunk,
                "target_structure_two": None,
                "target_word": target_word,
            },
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    @property
    def target_structures(self):
        return StructureCollection(
            {
                self.target_view,
                self.target_word,
                self.target_structure_one,
                self.target_structure_two,
            }
        )

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_word = self._target_structures["target_word"]
        self.target_structure_one = self._target_structures["target_structure_one"]
        self.target_structure_two = self._target_structures["target_structure_two"]
        self.conceptual_space = (
            self.target_word.lexeme.concepts.get_random()
            .parent_spaces.where(no_of_dimensions=1)
            .get_random()
        )
        self.parent_concept = (
            self.bubble_chamber.spaces["relational concepts"]
            .contents.of_type(Space)
            .get_random()
            .contents.of_type(Concept)
            .get_random()
        )
        self._target_structures["parent_concept"] = self.parent_concept
        self.target_space = self.conceptual_space.instance_in_space(
            self.target_view.interpretation_space
        )
        self._target_structures["target_space"] = self.target_space
        target_structure_one_corresponding_word = (
            self.target_structure_one.correspondences_to_space(
                self.target_view.text_space
            )
            .get_random()
            .arguments.get_random(exclude=[self.target_structure_one])
        )
        if self.target_structure_two is None:
            try:
                target_structure_two_corresponding_word = (
                    self.target_word.potential_argument_words.get_exigent(
                        exclude=[target_structure_one_corresponding_word]
                    )
                )
                self.target_structure_two = (
                    target_structure_two_corresponding_word.correspondences_to_space(
                        self.target_view.interpretation_space
                    )
                    .get_random()
                    .arguments.get_random(
                        exclude=[target_structure_two_corresponding_word]
                    )
                )
                self._target_structures[
                    "target_structure_two"
                ] = self.target_structure_two
            except MissingStructureError:
                return False
        return not self.target_structure_one.has_relation(
            self.target_space,
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
        ) and not self.target_word.has_correspondence_to_space(
            self.target_view.interpretation_space
        )

    def _calculate_confidence(self):
        target_word_concept = self.target_word.lexeme.concepts.get_random()
        self.confidence = (
            target_word_concept.relations_with(self.parent_concept)
            .get_random()
            .activation
        )
