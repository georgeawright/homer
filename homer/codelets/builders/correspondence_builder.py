from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID


class CorrespondenceBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_view = target_structures.get("target_view")
        self.target_space_one = target_structures.get("target_space_one")
        self.target_structure_one = target_structures.get("target_structure_one")
        self.target_space_two = target_structures.get("target_space_two")
        self.target_structure_two = target_structures.get("target_structure_two")
        self.target_conceptual_space = target_structures.get("target_conceptual_space")
        self.parent_concept = target_structures.get("parent_concept")
        self.target_sub_view = target_structures.get("target_sub_view")
        self.sub_frame = target_structures.get("sub_frame")
        self.correspondence = None
        self.child_structure = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators import CorrespondenceEvaluator

        return CorrespondenceEvaluator

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
        return self.bubble_chamber.concepts["correspondence"]

    @property
    def targets_dict(self):
        return {
            "target_structure_one": self.target_structure_one,
            "target_structure_two": self.target_structure_two,
            "target_space_one": self.target_space_one,
            "target_space_two": self.target_space_two,
            "target_conceptual_space": self.target_conceptual_space,
            "parent_concept": self.parent_concept,
            "sub_frame": self.sub_frame,
            "target_view": self.target_view,
            "target_sub_view": self.target_sub_view,
        }

    def _passes_preliminary_checks(self):
        return self.target_view.can_accept_member(
            self.parent_concept,
            self.target_conceptual_space,
            self.target_structure_one,
            self.target_structure_two,
        )

    def _process_structure(self):
        raise NotImplementedError

    def _fizzle(self):
        pass

    def _add_contextual_space_correspondence(self):
        sub_frame_correspondence = self.child_structures.get()
        try:
            contextual_space_to_sub_frame_correspondence = (
                self.target_structure_one.correspondences.filter(
                    lambda x: x.end == self.target_structure_one
                    and x.start.parent_space in self.target_view.input_spaces
                ).get()
            )
            contextual_space_structure = (
                contextual_space_to_sub_frame_correspondence.start
            )
        except MissingStructureError:
            try:
                contextual_space_to_sub_frame_correspondence = (
                    self.target_structure_one.correspondences.filter(
                        lambda x: x.start == self.target_structure_one
                        and not x.end.is_slot
                    ).get(exclude=[sub_frame_correspondence])
                )
                contextual_space_structure = (
                    (contextual_space_to_sub_frame_correspondence.end)
                    if contextual_space_to_sub_frame_correspondence.end
                    != self.target_structure_two
                    else None
                )
            except MissingStructureError:
                contextual_space_structure = None
        if contextual_space_structure is not None:
            contextual_space = contextual_space_structure.parent_space
            contextual_space_correspondence = self.bubble_chamber.new_correspondence(
                parent_id=self.codelet_id,
                start=contextual_space_structure,
                end=self.target_structure_two,
                locations=[
                    contextual_space_structure.location_in_space(contextual_space),
                    self.target_structure_two.location_in_space(self.target_space_two),
                ],
                parent_concept=self.parent_concept,
                conceptual_space=self.target_conceptual_space,
                parent_view=self.target_view,
            )
            self._structure_concept.instances.add(contextual_space_correspondence)
            self._structure_concept.recalculate_exigency()
            self.child_structures.add(contextual_space_correspondence)
