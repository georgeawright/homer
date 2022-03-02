from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection_keys import (
    activation,
    corresponding_exigency,
    exigency,
    uncorrespondedness,
)
from homer.structures.links import Correspondence
from homer.structures.nodes import Concept


class SpaceToFrameCorrespondenceSuggester(CorrespondenceSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.correspondence_builders import (
            SpaceToFrameCorrespondenceBuilder,
        )

        return SpaceToFrameCorrespondenceBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.production_views.get(key=exigency)
        target_space_two = target_view.parent_frame.input_space
        target_structure_two = target_space_two.contents.where(
            is_correspondence=False
        ).get(key=uncorrespondedness)
        urgency = (
            urgency if urgency is not None else target_structure_two.uncorrespondedness
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_space_two": target_space_two,
                "target_structure_two": target_structure_two,
            },
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
        target_view = bubble_chamber.production_views.get(key=activation)
        target_space_two = target_view.parent_frame.input_space
        target_structure_two = target_space_two.contents.where(
            is_correspondence=False
        ).get(key=uncorrespondedness)
        urgency = (
            urgency if urgency is not None else target_structure_two.uncorrespondedness
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_space_two": target_space_two,
                "target_structure_two": target_structure_two,
                "parent_concept": parent_concept,
            },
            urgency,
        )

    def _passes_preliminary_checks(self):
        self._get_target_conceptual_space()
        try:
            if self.target_space_one is None:
                self.target_space_one = self.target_view.input_spaces.get()
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found target space one: {self.target_space_one}"
                )
            if self.target_structure_one is None:
                self._get_target_structure_one()
        except MissingStructureError:
            self.bubble_chamber.loggers["activity"].log(
                self,
                "MissingStructureError when searching for input target space and structure",
            )
            return False
        self.parent_concept = self.bubble_chamber.concepts["same"]
        self.bubble_chamber.loggers["activity"].log(
            self, f"Found parent concept: {self.parent_concept}"
        )
        if not self.target_view.can_accept_member(
            self.parent_concept,
            self.target_conceptual_space,
            self.target_structure_one,
            self.target_structure_two,
        ):
            self.bubble_chamber.loggers["activity"].log(
                self, "Target view cannot accept suggested member."
            )
            return False
        return True

    def _fizzle(self):
        from .potential_sub_frame_to_frame_correspondence_suggester import (
            PotentialSubFrameToFrameCorrespondenceSuggester,
        )

        try:
            return PotentialSubFrameToFrameCorrespondenceSuggester.make(
                self.codelet_id, self.bubble_chamber
            )
        except MissingStructureError:
            pass
