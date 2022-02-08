from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection_keys import activation
from homer.structures.nodes import Concept


class SpaceSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.projectable_space = target_structures.get("projectable_space")
        self.metaphor_space = target_structures.get("metaphor_space")

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders import SpaceBuilder

        return SpaceBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = (
            "TopDown" if target_structures["metaphor_space"] is not None else "BottomUp"
        )
        codelet_id = ID.new(cls, qualifier)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        projectable_space = bubble_chamber.conceptual_spaces.filter(
            lambda space: not space.contents.where(is_concept=True)
            .filter(lambda concept: not concept.correspondences.is_empty())
            .is_empty()
        ).get(key=activation)
        concept = projectable_space.contents.where(is_concept=True).get(key=activation)
        metaphor_space = concept.correspondees.get().parent_space
        if not projectable_space.correspondees.where(
            parent_concept=metaphor_space.parent_concept
        ).is_empty():
            urgency = 0
        else:
            urgency = urgency if urgency is not None else concept.activation
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {"projectable_space": projectable_space, "metaphor_space": metaphor_space},
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        return cls.make(parent_id, bubble_chamber, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["space-conceptual"]

    @property
    def targets_dict(self):
        return {
            "projectable_space": self.projectable_space,
            "metaphor_space": self.metaphor_space,
        }

    def _passes_preliminary_checks(self):
        if self.metaphor_space is None:
            self.metaphor_space = self.bubble_chamber.conceptual_spaces.filter(
                lambda x: not x.contents.where(is_concept=True)
                .filter(lambda y: y.has_correspondence_to_space(self.projectable_space))
                .is_empty()
            ).get()
        elif (
            self.metaphor_space.contents.where(is_concept=True)
            .filter(lambda x: x.has_correspondence_to_space(self.projectable_space))
            .is_empty()
        ):
            return False
        return self.projectable_space.correspondees.where(
            parent_concept=self.metaphor_space.parent_concept
        ).is_empty()

    def _calculate_confidence(self):
        self.confidence = self.metaphor_space.parent_concept.depth

    def _fizzle(self):
        pass
