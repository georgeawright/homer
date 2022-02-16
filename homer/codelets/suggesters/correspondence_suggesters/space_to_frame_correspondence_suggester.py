from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection_keys import activation, corresponding_exigency, exigency
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
        target_space = target_view.input_contextual_spaces.get()
        target = target_space.contents.where(is_correspondence=False).get(
            key=corresponding_exigency
        )
        urgency = urgency if urgency is not None else target.uncorrespondedness
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_space_one": target_space,
                "target_structure_one": target,
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
        target_space = target_view.input_contextual_spaces.get()
        target = target_space.contents.where(is_link=True, is_correspondence=False).get(
            key=corresponding_exigency
        )
        urgency = urgency if urgency is not None else target.uncorrespondedness
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_space_one": target_space,
                "target_structure_one": target,
                "parent_concept": parent_concept,
            },
            urgency,
        )

    def _passes_preliminary_checks(self):
        self.target_conceptual_space = (
            self.target_structure_one.parent_concept.parent_space
            if self.target_structure_one.is_link
            else None
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Found conceptual space: {self.target_conceptual_space}"
        )
        try:
            if self.target_space_two is None:
                self.target_space_two = self.target_view.parent_frame.input_space
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found target space two: {self.target_space_two}"
                )
            if self.target_structure_two is None:
                self.target_structure_two = self.target_space_two.contents.filter(
                    lambda x: (type(x) == type(self.target_structure_one))
                    and (
                        x.has_location_in_space(self.target_conceptual_space)
                        if self.target_conceptual_space is not None
                        else True
                    )
                ).get(key=lambda x: x.similarity_with(self.target_structure_one))
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found target structure two: {self.target_structure_two}"
                )
        except MissingStructureError:
            self.bubble_chamber.loggers["activity"].log(
                self,
                "MissingStructureError when searching for second target space and structure",
            )
            return False
        if self.parent_concept is None:
            self.parent_concept = (
                self.bubble_chamber.concepts.where(structure_type=Correspondence)
                .where_not(classifier=None)
                .get()
            )
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

        return PotentialSubFrameToFrameCorrespondenceSuggester.make(
            self.codelet_id, self.bubble_chamber
        )
