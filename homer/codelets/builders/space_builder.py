from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID


class SpaceBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.projectable_space = target_structures.get("projectable_space")
        self.metaphor_space = target_structures.get("metaphor_space")

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators import SpaceEvaluator

        return SpaceEvaluator

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
        return self.bubble_chamber.concepts["conceptual-space"]

    @property
    def targets_dict(self):
        return {
            "projectable_space": self.projectable_space,
            "metaphor_space": self.metaphor_space,
        }

    def _passes_preliminary_checks(self):
        return self.projectable_space.correspondees.where(
            parent_concept=self.metaphor_space.parent_concept
        ).is_empty()

    def _process_structure(self):
        space = self.bubble_chamber.new_conceptual_space()
        correspondence = self.bubble_chamber.new_correspondence()
        # give metaphor space concepts locations in new space
        self.child_structures = self.bubble_chamber.new_structure_collection(
            space, correspondence
        )

    def _fizzle(self):
        pass
