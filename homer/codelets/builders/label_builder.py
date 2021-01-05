from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structures import Chunk, Concept
from homer.structures.links import Label
from homer.structures.spaces import ConceptualSpace
from homer.tools import project_item_into_space


class LabelBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
        parent_concept: Concept = None,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_chunk = target_chunk
        self.parent_concept = parent_concept
        self.child_structure = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
        parent_concept: Concept = None,
    ):
        qualifier = "TopDown" if parent_concept is not None else "BottomUp"
        codelet_id = ID.new(cls, qualifier)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_chunk,
            urgency,
            parent_concept,
        )

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target = bubble_chamber.chunks.get_unhappy()
        return cls.spawn(parent_id, bubble_chamber, target, target.unhappiness)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        if self.parent_concept is None:
            self.parent_concept = (
                self.bubble_chamber.spaces["label concepts"]
                .contents.of_type(ConceptualSpace)
                .where(is_basic_level=True)
                .get_random()
                .contents.of_type(Concept)
                .get_random()
            )
        return not self.target_chunk.has_label(self.parent_concept)

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            {"concept": self.parent_concept, "start": self.target_chunk}
        )

    def _process_structure(self):
        space = self.parent_concept.parent_space.instance
        self.bubble_chamber.logger.log(space)
        if self.target_chunk not in space.contents:
            project_item_into_space(self.target_chunk, space)
        label = Label(
            ID.new(Label),
            self.codelet_id,
            self.target_chunk,
            self.parent_concept,
            space,
            0,
        )
        label.activation = self.INITIAL_STRUCTURE_ACTIVATION
        space.add(label)
        self.target_chunk.links_out.add(label)
        self.bubble_chamber.labels.add(label)
        self.bubble_chamber.working_spaces.add(space)
        top_level_working_space = self.bubble_chamber.spaces["top level working"]
        space.locations.append(Location([], top_level_working_space))
        top_level_working_space.add(space)
        space.parent_spaces.add(self.bubble_chamber.spaces["top level working"])
        self.child_structure = label
        self.bubble_chamber.logger.log(self.child_structure)

    def _engender_follow_up(self):
        from homer.codelets.evaluators import LabelEvaluator

        self.child_codelets.append(
            LabelEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.child_structure,
                self.confidence,
            )
        )

    def _fizzle(self):
        self._re_engender()

    def _fail(self):
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
