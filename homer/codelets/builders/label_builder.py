from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structures import Chunk, Concept
from homer.structures.links import Label


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

    @property
    def _parent_link(self):
        label = self.bubble_chamber.concepts["label"]
        build = self.bubble_chamber.concepts["build"]
        return label.relations_with(build).get_random()

    def _passes_preliminary_checks(self):
        if self.parent_concept is None:
            self.parent_concept = (
                self.bubble_chamber.spaces["label concepts"]
                .contents.get_random()
                .child_spaces.get_random()
                .contents.get_random()
            )
        return not self.target_chunk.has_label(self.parent_concept)

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            {"concept": self.parent_concept, "start": self.target_chunk}
        )

    def _process_structure(self):
        space = self.parent_concept.parent_space.instance
        self.bubble_chamber.logger.log(space)
        label = Label(
            ID.new(Label),
            self.codelet_id,
            self.target_chunk,
            self.parent_concept,
            space,
            self.confidence,
        )
        if self.target_chunk not in space.contents:
            space.contents.add(self.target_chunk)
            self.target_chunk.parent_spaces.add(space)
            self.target_chunk.locations.append(
                Location(
                    getattr(self.target_chunk, self.parent_concept.relevant_value),
                    space,
                )
            )
        space.contents.add(label)
        self.target_chunk.links_out.add(label)
        self.bubble_chamber.labels.add(label)
        self.bubble_chamber.spaces.add(space)
        self.child_structure = label
        self.bubble_chamber.logger.log(self.child_structure)

    def _engender_follow_up(self):
        new_target = self.target_chunk.neighbours.get_unhappy()
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
