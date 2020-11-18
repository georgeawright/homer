from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
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
        codelet_id = ID.new(cls)
        return cls(
            codelet_id, parent_id, bubble_chamber, input_space, output_space, urgency
        )

    def _passes_preliminary_checks(self):
        self.template_word = self.input_space.contents.get_unhappy()
        for word in self.output_space.contents:
            if len(word.correspondences_with(self.template_word)) > 0:
                return False
        return True

    def _boost_activations(self):
        pass

    def _calculate_confidence(self):
        self.confidence = 1.0

    def _process_structure(self):
        output_word = Word(
            self.template_word.value,
            self.template_word.location,
            StructureCollection({self.output_space}),
            self.confidence,
        )
        self.output_space.contents.add(output_word)
        correspondence_space = self.bubble_chamber.common_parent_space(
            self.input_space, self.output_space
        )
        correspondence = Correspondence(
            self.template_word,
            output_word,
            self.input_space,
            self.output_space,
            self.bubble_chamber.concepts["same"],
            correspondence_space,
            self.bubble_chamber.spaces["text"],
            self.confidence,
        )
        self.template_word.links_out.add(correspondence)
        output_word.links_in.add(correspondence)
        correspondence_space.contents.add(correspondence)
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
