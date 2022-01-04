from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation, corresponding_exigency
from homer.structures.nodes import Concept
from homer.structures.links import Correspondence

# TODO: suggest a corresp between input space structure and mainframe slot
# this should only happen for structures not in a sub-frame
# builder needs to fill in slot

# TODO: or suggest a corresp between mainframe and subframe structures
# builder needs to fill in slot
# builder should build multiple correspondences subframe-mainframe and inputspace-mainframe
# also needs to build chunk-chunk and letterchunk-letterchunk correspondences

# TODO: or suggest a corresp between a mainframe structure and a potential subframe's structure
# builder needs to add new subframe and another view's correspondences to view (either destroy view and change correspondences' parent view or make view a sub-view)


class CorrespondenceSuggester(Suggester):
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
        self.target_view = target_structures.get("target_view")
        self.target_structure_one = target_structures.get("target_structure_one")
        self.target_structure_two = target_structures.get("target_structure_two")
        self.target_space_one = target_structures.get("target_space_one")
        self.target_space_two = target_structures.get("target_space_two")
        self.target_conceptual_space = target_structures.get("target_conceptual_space")
        self.parent_concept = target_structures.get("parent_concept")
        self.correspondence = None
        self.child_structure = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders import CorrespondenceBuilder

        return CorrespondenceBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = (
            "TopDown" if target_structures["parent_concept"] is not None else "BottomUp"
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
                "target_space_two": None,
                "target_structure_two": None,
                "target_conceptual_space": None,
                "parent_concept": None,
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
                "target_space_two": None,
                "target_structure_two": None,
                "target_conceptual_space": None,
                "parent_concept": parent_concept,
            },
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    @property
    def target_dict(self):
        return {
            "target_structure_one": self.target_structure_one,
            "target_structure_two": self.target_structure_two,
            "target_space_one": self.target_space_two,
            "target_space_two": self.target_space_two,
            "target_conceptual_space": self.target_conceptual_space,
            "parent_concept": self.parent_concept,
            "target_view": self.target_view,
        }

    def _passes_preliminary_checks(self):
        raise NotImplementedError
        # TODO: also needs to be possible to construct correspondence from small frame element to big frame element
        if self.target_space_two is None:
            try:
                self.target_space_two = self.target_view.parent_frame.input_space
            except MissingStructureError:
                try:
                    self.target_space_two = self.target_view.input_spaces.get(
                        key=activation, exclude=[self.target_space_one]
                    )
                except MissingStructureError:
                    return False
        try:
            if self.target_structure_two is None:
                self.target_structure_two = self.target_space_two.contents.of_type(
                    type(self.target_structure_one)
                ).get(key=lambda x: x.similarity_with(self.target_structure_one))
        except MissingStructureError:
            return False
        if self.target_conceptual_space is None:
            try:
                self.target_conceptual_space = (
                    StructureCollection.union(
                        self.target_structure_one.parent_spaces,
                        self.target_structure_two.parent_spaces,
                    )
                    .where(is_basic_level=True)
                    .get()
                )
            except MissingStructureError:
                return False
        if self.parent_concept is None:
            self.parent_concept = self.bubble_chamber.concepts.where(
                structure_type=Correspondence
            ).get()
        if self.target_view.has_member(
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
            self.target_space_one,
            self.target_space_two,
        ):
            return False
        self.correspondence = Correspondence(
            None,
            self.codelet_id,
            self.target_structure_one,
            self.bubble_chamber.new_structure_collection(
                self.target_structure_one, self.target_structure_two
            ),
            [
                self.target_structure_one.location_in_space(self.target_space_one),
                self.target_structure_two.location_in_space(self.target_space_two),
            ],
            self.parent_concept,
            self.target_conceptual_space,
            self.target_view,
            0,
            links_in=self.bubble_chamber.new_structure_collection(),
            links_out=self.bubble_chamber.new_structure_collection(),
            parent_spaces=self.bubble_chamber.new_structure_collection(),
        )
        return self.target_view.can_accept_member(self.correspondence)

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            concept=self.parent_concept,
            space=self.target_conceptual_space,
            start=self.target_structure_one,
            end=self.target_structure_two,
            view=self.target_view,
        )

    def _fizzle(self):
        pass
