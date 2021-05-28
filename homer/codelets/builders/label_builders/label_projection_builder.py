import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import LabelBuilder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label
from homer.tools import project_item_into_space


class LabelProjectionBuilder(LabelBuilder):
    """Builds a label in a new space with a correspondence to a node in another space.
    Sets the value or coordinates of the chunk according to the parent concept's prototyp."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        LabelBuilder.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_view = None
        self.target_chunk = None
        self.target_word = None
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

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["label"]

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_chunk = self._target_structures["target_chunk"]
        self.target_word = self._target_structures["target_word"]
        try:
            self.parent_concept = self.target_word.lexeme.concepts.get()
        except MissingStructureError:
            return False
        return not self.target_chunk.has_label(self.parent_concept) and all(
            not isinstance(
                correspondence.arguments.get(exclude=[self.target_word]), Label
            )
            for correspondence in self.target_word.correspondences_to_space(
                self.target_view.interpretation_space
            )
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
                ).coordinates = self.parent_concept.value
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
