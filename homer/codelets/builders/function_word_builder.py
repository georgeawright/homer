from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structures import Space
from homer.structures.chunks import Word
from homer.structures.links import Correspondence


class FunctionWordBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        input_space: Space,
        output_space: Space,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.input_space = input_space
        self.output_space = output_space
        self.child_structure = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        input_space: Space,
        output_space: Space,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ""
        return cls(
            codelet_id, parent_id, bubble_chamber, input_space, output_space, urgency
        )

    def _passes_preliminary_checks(self):
        return True

    def _boost_activations(self):
        pass

    def _calculate_confidence(self):
        self.confidence = 1.0

    def _process_structure(self):
        template_word = self.input_space.words.get_unhappy()
        output_word = Word(
            template_word.value, template_word.location, self.output_space
        )
        self.output_space.contents.add(output_word)
        correspondence = Correspondence(
            template_word, output_word, self.bubble_chamber.concepts["same"]
        )
        template_word.links_out.add(correspondence)
        output_word.links_in.add(correspondence)
        self.bubble_chamber.correspondences.add(correspondence)
        self.child_structure = output_word

    def _fizzle(self):
        pass

    def _fail(self):
        pass

    def _engender_follow_up(self):
        self.child_codelets.append(
            FunctionWordBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.input_space,
                self.output_space,
                self.urgency,
            )
        )
