from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structures.chunk import Chunk
from homer.structures.concept import Concept


class LabelBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        structure_concept: Concept,
        bubble_chamber: BubbleChamber,
        target_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
        parent_concept: Concept = None,
    ):
        Builder.__init__(self, codelet_id, parent_id, urgency)
        self.structure_concept = structure_concept
        self.bubble_chamber = bubble_chamber
        self.target_chunk = target_chunk
        self.parent_concept = parent_concept
        self.confidence = 0.0
        self.child_perceptlet = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
        parent_concept: Concept = None,
    ):
        codelet_id = ""
        structure_concept = bubble_chamber.concepts["label"]
        return cls(
            codelet_id,
            parent_id,
            structure_concept,
            bubble_chamber,
            target_chunk,
            urgency,
            parent_concept,
        )

    def _passes_preliminary_checks(self):
        if self.parent_concept is None:
            self.parent_concept = self.bubble_chamber.get_random_workspace_concept()
        return not self.target_perceptlet.has_label(self.parent_concept)

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classify(self.target_chunk)

    def _boost_activations(self):
        pass

    def _process_perceptlet(self):
        label = self.bubble_chamber.create_label(
            self.parent_concept,
            self.target_perceptlet.location,
            self.target_perceptlet,
            self.confidence,
            self.codelet_id,
        )
        self.target_perceptlet.add_label(label)
        self.bubble_chamber.logger.log_perceptlet_connection(
            self, self.target_perceptlet, label
        )
        self.child_perceptlet = label

    def _engender_follow_up(self):
        new_target = self.target_perceptlet.neighbours.get_unhappy()
        self.child_codelets.append(
            LabelBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                new_target,
                self.confidence,
                self.parent_concept,
            )
        )

    def _fizzle(self):
        self._re_engender()

    def _fail(self):
        self._decay_concept(self.parent_concept)
        self._re_engender()

    def _re_engender(self):
        self.child_codelets.append(
            LabelBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_chunk,
                self.target_chunk.unhappiness,
            )
        )
