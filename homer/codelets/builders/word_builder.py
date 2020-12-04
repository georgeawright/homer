from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.chunks import Word, Slot, View
from homer.structures.links import Correspondence

from .function_word_builder import FunctionWordBuilder


class WordBuilder(Builder):
    """Builds a correspondence and a new item in an output space connected to it."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_correspondence: Correspondence,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_view = target_view
        self.target_correspondence = target_correspondence
        self.child_structure = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_correspondence: Correspondence,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_view,
            target_correspondence,
            urgency,
        )

    @property
    def _parent_link(self):
        word = self.bubble_chamber.concepts["word"]
        build = self.bubble_chamber.concepts["build"]
        return word.relations_with(build).get_random()

    def _passes_preliminary_checks(self):
        self.slot = self.target_correspondence.get_slot_argument()
        self.non_slot = self.target_correspondence.get_non_slot_argument()
        self.slot_space = (
            self.target_correspondence.start_space
            if self.slot == self.target_correspondence.start
            else self.target_correspondence.end_space
        )
        self.non_slot_space = (
            self.target_correspondence.end_space
            if self.slot_space == self.target_correspondence.start_space
            else self.target_correspondence.start_space
        )
        self.output_space = self.target_view.output_space
        for word in self.output_space.contents:
            if len(word.correspondences_with(self.slot)) > 0:
                return False
        return True

    def _calculate_confidence(self):
        self.confidence = self.target_correspondence.activation

    def _process_structure(self):
        concept = self.non_slot.labels.get_active().parent_concept
        lexeme = concept.lexemes.get_active()
        word_value = lexeme.get_form(self.slot.form)
        word_location = self.slot.location
        word = Word(
            ID.new(Word),
            self.codelet_id,
            word_value,
            word_location,
            StructureCollection({self.output_space}),
            self.confidence,
        )
        slot_to_word_space = self.bubble_chamber.common_parent_space(
            self.slot_space, self.output_space
        )
        projection_from_slot = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            self.slot,
            word,
            self.slot_space,
            self.output_space,
            self.bubble_chamber.concepts["same"],
            slot_to_word_space,
            concept.parent_space,
            self.confidence,
        )
        self.slot.links_out.add(projection_from_slot)
        word.links_in.add(projection_from_slot)
        slot_to_word_space.contents.add(projection_from_slot)
        self.bubble_chamber.correspondences.add(projection_from_slot)
        self.target_view.members.add(projection_from_slot)
        non_slot_to_word_space = self.bubble_chamber.common_parent_space(
            self.non_slot_space, self.output_space
        )
        projection_from_non_slot = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            self.non_slot,
            word,
            self.non_slot_space,
            self.output_space,
            self.bubble_chamber.concepts["same"],
            non_slot_to_word_space,
            concept.parent_space,
            self.confidence,
        )
        self.non_slot.links_out.add(projection_from_non_slot)
        word.links_in.add(projection_from_non_slot)
        non_slot_to_word_space.contents.add(projection_from_non_slot)
        self.bubble_chamber.correspondences.add(projection_from_non_slot)
        self.target_view.members.add(projection_from_non_slot)
        self.output_space.contents.add(word)
        self.bubble_chamber.words.add(word)
        self.child_structure = word

    def _engender_follow_up(self):
        self.child_codelets.append(
            FunctionWordBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.slot.parent_spaces.get_random(),
                self.output_space,
                self.confidence,
            )
        )

    def _fizzle(self):
        pass

    def _fail(self):
        pass
