from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
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
        Builder.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.target_view = target_view
        self.target_correspondence = target_correspondence
        self.confidence = 0.0
        self.child_structure = None

    def _passes_preliminary_checks(self):
        self.slot = self.target_correspondence.get_slot_argument()
        self.non_slot = self.target_correspondence.get_non_slot_argument()
        self.output_space = self.target_view.output_space
        return True

    def _calculate_confidence(self):
        self.confidence = self.target_correspondence.activation

    def _boost_activations(self):
        pass

    def _process_structure(self):
        concept = self.non_slot.labels.get_active().parent_concept
        lexeme = concept.lexemes.get_active()
        word_value = lexeme.get_form(self.slot.form)
        word_location = self.slot.location
        word = Word(word_value, word_location, self.output_space)
        projection_from_slot = Correspondence(
            self.slot, word, self.bubble_chamber.concepts["same"]
        )
        self.slot.links_out.add(projection_from_slot)
        word.links_in.add(projection_from_slot)
        self.target_view.add_correspondence(projection_from_slot)
        projection_from_non_slot = Correspondence(
            self.non_slot, word, self.bubble_chamber.concepts["same"]
        )
        self.non_slot.links_out.add(projection_from_non_slot)
        word.links_in.add(projection_from_non_slot)
        self.target_view.add_correspondence(projection_from_non_slot)
        self.output_space.add_word(word)
        self.child_structure = word

    def _engender_follow_up(self):
        self.child_codelets.append(
            FunctionWordBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.slot.parent_space,
                self.output_space,
                self.confidence,
            )
        )

    def _fizzle(self):
        pass

    def _fail(self):
        pass
