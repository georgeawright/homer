import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import LabelBuilder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Correspondence, Label
from homer.structures.nodes import Chunk, Word
from homer.tools import project_item_into_space


class LabelProjectionBuilder(LabelBuilder):
    """Builds a label in a new space with a correspondence to a node in another space.
    Sets the value or coordinates of the chunk according to the parent concept's prototyp."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_chunk: Chunk,
        target_word: Word,
        urgency: FloatBetweenOneAndZero,
    ):
        LabelBuilder.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_chunk, urgency
        )
        self.target_view = target_view
        self.target_chunk = target_chunk
        self.target_word = target_word
        self.parent_concept = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.label_evaluators import LabelProjectionEvaluator

        return LabelProjectionEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_chunk: Chunk,
        target_word: Word,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_view,
            target_chunk,
            target_word,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.monitoring_views.get_active()
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
            parent_id, bubble_chamber, target_view, target_chunk, target_word, urgency
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        self.parent_concept = self.target_word.lexeme.concepts.get_random()
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

    def _process_structure(self):
        space = self.parent_concept.parent_space.instance_in_space(
            self.target_view.interpretation_space
        )
        self.bubble_chamber.logger.log(space)
        if self.target_chunk not in space.contents:
            if self.parent_concept.relevant_value == "value":
                self.target_chunk.value = self.parent_concept.value
            elif self.parent_concept.relevant_value == "coordinates":
                self.target_chunk.location_in_space(
                    self.target_view.interpretation_space
                ).coordinates = self.parent_concept.coordinates
            project_item_into_space(self.target_chunk, space)
        label = Label(
            structure_id=ID.new(Label),
            parent_id=self.codelet_id,
            start=self.target_chunk,
            parent_concept=self.parent_concept,
            parent_space=space,
            quality=0,
        )
        self.target_chunk.links_out.add(label)
        start_space = self.target_word.parent_space
        end_space = space
        correspondence = Correspondence(
            structure_id=ID.new(Correspondence),
            parent_id=self.codelet_id,
            start=self.target_word,
            end=label,
            start_space=start_space,
            end_space=end_space,
            locations=[self.target_word.location, label.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=space.conceptual_space,
            parent_view=self.target_view,
            quality=0,
        )
        label.links_out.add(correspondence)
        label.links_in.add(correspondence)
        self.target_word.links_out.add(correspondence)
        self.target_word.links_in.add(correspondence)
        start_space.add(correspondence)
        end_space.add(correspondence)
        self.target_view.members.add(correspondence)
        self.bubble_chamber.correspondences.add(correspondence)
        self.bubble_chamber.logger.log(correspondence)
        self.bubble_chamber.logger.log(self.target_view)
        self.child_structures = StructureCollection({label, correspondence})

    def _fizzle(self):
        self._re_engender()

    def _fail(self):
        self._re_engender()

    def _re_engender(self):
        self.child_codelets.append(
            self.make(self.codelet_id, self.bubble_chamber, urgency=self.urgency / 2)
        )
