from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets import Factory
from homer.codelets.suggesters import LabelSuggester, RelationSuggester
from homer.codelets.suggesters.correspondence_suggesters import (
    PotentialSubFrameToFrameCorrespondenceSuggester,
    SpaceToFrameCorrespondenceSuggester,
    SubFrameToFrameCorrespondenceSuggester,
)
from homer.codelets.suggesters.projection_suggesters import (
    ChunkProjectionSuggester,
    LabelProjectionSuggester,
    LetterChunkProjectionSuggester,
    RelationProjectionSuggester,
)
from homer.codelets.suggesters.view_suggesters import SimplexViewSuggester
from homer.errors import MissingStructureError, NoLocationError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection_keys import (
    activation,
    exigency,
    labeling_exigency,
    uncorrespondedness,
)
from homer.structures import View
from homer.structures.links import Relation


class ViewDrivenFactory(Factory):
    """Finds a view with unfilled slots
    and spawns a codelet to suggest a structure that could fill a slot"""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
        target_view: View = None,
    ):
        Factory.__init__(self, codelet_id, parent_id, bubble_chamber, coderack, urgency)
        self.target_view = target_view
        self.target_slot = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
        target_view: View = None,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id, parent_id, bubble_chamber, coderack, urgency, target_view
        )

    def follow_up_urgency(self) -> FloatBetweenOneAndZero:
        urgency = (
            self.bubble_chamber.focus.view.unhappiness
            if self.bubble_chamber.focus.view is not None
            else 1 - self.bubble_chamber.satisfaction
        )
        if urgency > self.coderack.MINIMUM_CODELET_URGENCY:
            return urgency
        return self.coderack.MINIMUM_CODELET_URGENCY

    def _engender_follow_up(self):
        from homer.codelets import FocusSetter

        if self.target_view is None:
            self.target_view = (
                self.bubble_chamber.focus.view
                if self.bubble_chamber.focus.view is not None
                else self.bubble_chamber.production_views.get(key=exigency)
            )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Targeting view {self.target_view}"
        )
        input_structures = self.target_view.parent_frame.input_space.contents.filter(
            lambda x: not x.is_correspondence and x.correspondences.is_empty()
        )
        try:
            self.target_slot = input_structures.get(key=uncorrespondedness)
        except MissingStructureError:
            output_structures = (
                self.target_view.parent_frame.output_space.contents.filter(
                    lambda x: not x.is_correspondence and x.correspondences.is_empty()
                )
            )
            self.bubble_chamber.loggers["activity"].log_collection(
                self, output_structures, "Uncorrespondended output structures"
            )
            try:
                self.target_slot = output_structures.where(is_chunk=True).get(
                    key=uncorrespondedness
                )
            except MissingStructureError:
                self.target_slot = output_structures.get(key=uncorrespondedness)
            follow_up = FocusSetter.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                1 - self.bubble_chamber.satisfaction,
            )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Targeting slot {self.target_slot}"
        )
        if self.target_slot.parent_space == self.target_view.parent_frame.input_space:
            try:
                follow_up = self._spawn_space_to_frame_correspondence_suggester()
            except MissingStructureError:
                follow_up = self._spawn_non_projection_suggester()
        elif (
            self.target_slot.parent_space == self.target_view.parent_frame.output_space
        ):
            follow_up = self._spawn_projection_suggester()
        else:  # slot is in sub-frame
            try:
                follow_up = self._spawn_sub_frame_to_frame_correspondence_suggester()
            except MissingStructureError:
                try:
                    follow_up = (
                        self._spawn_potential_sub_frame_to_frame_correspondence_suggester()
                    )
                except MissingStructureError:
                    try:
                        follow_up = self._spawn_view_driven_factory()
                    except MissingStructureError:
                        follow_up = self._spawn_simplex_view_suggester()
        self.child_codelets.append(follow_up)

    def _spawn_non_projection_suggester(self):
        input_space = self.target_view.input_spaces.get()
        if self.target_slot.is_label:
            node = None
            for node_group in self.target_view.node_groups:
                if (
                    input_space in node_group
                    and self.target_slot.start in node_group.values()
                ):
                    node = node_group[input_space]
                    break
            if node is None:
                if self.target_slot.is_link and self.target_slot.is_node:
                    node = input_space.contents.where(
                        is_labellable=True, is_slot=False
                    ).get(key=labeling_exigency)
                else:
                    node = input_space.contents.where(is_node=True, is_slot=False).get(
                        key=labeling_exigency
                    )
            parent_concept = (
                self.target_slot.parent_spaces.where(is_conceptual_space=True)
                .get()
                .contents.where(is_concept=True, is_slot=False)
                .get(key=lambda x: x.proximity_to(node))
            )
            return LabelSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {"target_node": node, "parent_concept": parent_concept},
                self.target_slot.uncorrespondedness,
            )
        if self.target_slot.is_relation:
            if self.target_slot.parent_concept.is_filled_in:
                parent_concept = self.target_slot.parent_concept.relatives.where(
                    is_slot=False
                ).get()
            else:
                parent_concept = (
                    self.target_slot.parent_spaces.filter(
                        lambda x: x.is_conceptual_space
                        and x.parent_concept.structure_type == Relation
                    )
                    .get()
                    .contents.where(is_concept=True, is_slot=False)
                    .get(key=activation)
                )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found parent concept {parent_concept}"
            )
            target_structure_one = None
            target_structure_two = None
            for node_group in self.target_view.node_groups:
                if (
                    input_space in node_group
                    and self.target_slot.start in node_group.values()
                ):
                    target_structure_one = node_group[input_space]
                if (
                    input_space in node_group
                    and self.target_slot.end in node_group.values()
                ):
                    target_structure_two = node_group[input_space]
            if target_structure_one is None or target_structure_two is None:
                potential_targets = input_space.contents.where(
                    is_node=True, is_slot=False
                )
                try:
                    (
                        target_structure_one,
                        target_structure_two,
                    ) = potential_targets.pairs.filter(
                        lambda x: (
                            x[0] == target_structure_one
                            if target_structure_one is not None
                            else True
                        )
                        and (
                            x[1] == target_structure_two
                            if target_structure_two is not None
                            else True
                        )
                    ).get(
                        key=lambda x: fuzzy.AND(
                            parent_concept.classifier.classify(
                                start=x[0],
                                end=x[1],
                                space=self.target_slot.conceptual_space,
                            ),
                            x[0].exigency,
                            x[1].exigency,
                        )
                    )
                except NoLocationError:
                    raise MissingStructureError
            return RelationSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "target_space": self.target_slot.conceptual_space,
                    "target_structure_one": target_structure_one,
                    "target_structure_two": target_structure_two,
                    "parent_concept": parent_concept,
                },
                self.target_slot.uncorrespondedness,
            )
        raise Exception("Slot is not a label or a relation.")

    def _spawn_projection_suggester(self):
        if self.target_slot.is_letter_chunk:
            follow_up_class = LetterChunkProjectionSuggester
        elif self.target_slot.is_chunk:
            follow_up_class = ChunkProjectionSuggester
        elif self.target_slot.is_label:
            follow_up_class = LabelProjectionSuggester
        elif self.target_slot.is_relation:
            follow_up_class = RelationProjectionSuggester
        return follow_up_class.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {"target_view": self.target_view, "target_projectee": self.target_slot},
            self.target_slot.uncorrespondedness
            if not self.target_slot.is_chunk
            else 1.0,
        )

    def _spawn_space_to_frame_correspondence_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            self, "Trying to build correspondence suggester"
        )
        follow_up = SpaceToFrameCorrespondenceSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {
                "target_view": self.target_view,
                "target_space_one": self.target_view.input_spaces.get(),
                "target_space_two": self.target_view.parent_frame.input_space,
                "target_structure_two": self.target_slot,
                "parent_concept": self.bubble_chamber.concepts["same"],
            },
            self.target_slot.uncorrespondedness,
        )
        self.bubble_chamber.loggers["activity"].log(self, f"follow_up: {follow_up}")
        follow_up._get_target_conceptual_space(self, follow_up)
        follow_up._get_target_structure_one(self, follow_up)
        return follow_up

    def _spawn_sub_frame_to_frame_correspondence_suggester(self):
        target_space_two = (
            self.target_view.parent_frame.input_space
            if self.target_slot in self.target_view.parent_frame.input_space.contents
            else self.target_view.parent_frame.output_space
        )
        sub_frame = self.target_view.parent_frame.sub_frames.filter(
            lambda x: x.input_space == self.target_slot.parent_space
            or x.output_space == self.target_slot.parent_space
        ).get()
        self.bubble_chamber.loggers["activity"].log_dict(
            self, self.target_view.matched_sub_frames, "view matched sub frames"
        )
        if sub_frame not in self.target_view.matched_sub_frames:
            raise MissingStructureError
        return SubFrameToFrameCorrespondenceSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {
                "target_view": self.target_view,
                "target_space_two": target_space_two,
                "target_structure_two": self.target_slot,
            },
            self.target_slot.uncorrespondedness,
        )

    def _spawn_potential_sub_frame_to_frame_correspondence_suggester(self):
        target_space_two = (
            self.target_view.parent_frame.input_space
            if self.target_slot in self.target_view.parent_frame.input_space.contents
            else self.target_view.parent_frame.output_space
        )
        sub_frame = self.target_view.parent_frame.sub_frames.filter(
            lambda x: x.input_space == self.target_slot.parent_space
            or x.output_space == self.target_slot.parent_space
        ).get()
        if self.bubble_chamber.production_views.filter(
            lambda x: x.parent_frame.parent_concept == sub_frame.parent_concept
        ).is_empty():
            raise MissingStructureError
        follow_up = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {
                "target_view": self.target_view,
                "target_space_two": target_space_two,
                "target_structure_two": self.target_slot,
                "sub_frame": sub_frame,
            },
            self.target_slot.uncorrespondedness,
        )
        follow_up._get_target_conceptual_space(self, follow_up)
        follow_up._get_target_space_one(self, follow_up)
        follow_up._get_target_structure_one(self, follow_up)
        return follow_up

    def _spawn_view_driven_factory(self):
        sub_frame = self.target_view.parent_frame.sub_frames.filter(
            lambda x: x.input_space == self.target_slot.parent_space
            or x.output_space == self.target_slot.parent_space
        ).get()
        contextual_space = self.target_view.input_spaces.get()
        prioritized_targets = self.bubble_chamber.new_structure_collection(
            *[
                group[contextual_space]
                for node in sub_frame.input_space.contents
                for group in self.target_view.node_groups
                if node in group.values()
            ]
        )
        views_with_correct_frame_and_spaces = (
            self.bubble_chamber.production_views.filter(
                lambda x: (x.parent_frame.parent_concept == sub_frame.parent_concept)
                and (x.input_spaces == self.target_view.input_spaces)
            )
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self,
            views_with_correct_frame_and_spaces,
            "Views with correct frame and spaces",
        )
        views_with_correct_prioritized_targets = (
            views_with_correct_frame_and_spaces.filter(
                lambda x: x.prioritized_targets == prioritized_targets
            )
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self,
            views_with_correct_prioritized_targets,
            "Views with correct priotitized_targets",
        )
        conceptual_space = None
        if self.target_slot.is_link and self.target_slot.is_node:
            conceptual_space = self.target_slot.parent_spaces.where(
                is_conceptual_space=True, is_basic_level=True
            ).get()
        elif self.target_slot.is_label:
            conceptual_space = self.target_slot.parent_concept.parent_space
        elif self.target_slot.is_relation:
            conceptual_space = self.target_slot.conceptual_space
        self.bubble_chamber.loggers["activity"].log(
            self, f"Conceptual space: {conceptual_space}"
        )
        views_with_correct_conceptual_space = (
            views_with_correct_prioritized_targets.filter(
                lambda x: (
                    conceptual_space in x.parent_frame.input_space.conceptual_spaces
                    if self.target_slot.parent_space == sub_frame.input_space
                    else conceptual_space
                    in x.parent_frame.output_space.contextual_spaces
                )
                or conceptual_space is None
            )
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, views_with_correct_conceptual_space, "Views with correct space"
        )
        target_sub_view = views_with_correct_conceptual_space.get(key=exigency)
        self.bubble_chamber.loggers["activity"].log(
            self, f"Found target sub view: {target_sub_view}"
        )
        return self.spawn(
            self.codelet_id,
            self.bubble_chamber,
            self.coderack,
            target_sub_view.exigency,
            target_view=target_sub_view,
        )

    def _spawn_simplex_view_suggester(self):
        sub_frame = self.target_view.parent_frame.sub_frames.filter(
            lambda x: x.input_space == self.target_slot.parent_space
            or x.output_space == self.target_slot.parent_space
        ).get()
        contextual_space = self.target_view.input_spaces.get()
        frame = self.bubble_chamber.frames.where(
            is_sub_frame=False, parent_concept=sub_frame.parent_concept
        ).get(key=activation)
        prioritized_targets = self.bubble_chamber.new_structure_collection(
            *[
                group[contextual_space]
                for node in sub_frame.input_space.contents
                for group in self.target_view.node_groups
                if node in group.values()
            ]
        )
        prioritized_conceptual_spaces = sub_frame.input_space.conceptual_spaces
        return SimplexViewSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {
                "frame": frame,
                "contextual_space": contextual_space,
                "prioritized_targets": prioritized_targets,
                "prioritized_conceptual_spaces": prioritized_conceptual_spaces,
            },
            self.target_slot.uncorrespondedness,
        )
