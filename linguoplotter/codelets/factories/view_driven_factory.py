from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Factory
from linguoplotter.codelets.suggesters import LabelSuggester, RelationSuggester
from linguoplotter.codelets.suggesters.correspondence_suggesters import (
    PotentialSubFrameToFrameCorrespondenceSuggester,
    SpaceToFrameCorrespondenceSuggester,
    SubFrameToFrameCorrespondenceSuggester,
)
from linguoplotter.codelets.suggesters.projection_suggesters import (
    ChunkProjectionSuggester,
    LabelProjectionSuggester,
    LetterChunkProjectionSuggester,
    RelationProjectionSuggester,
)
from linguoplotter.codelets.suggesters.view_suggesters import SimplexViewSuggester
from linguoplotter.errors import MissingStructureError, NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.id import ID
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structure_collection_keys import (
    activation,
    exigency,
    labeling_exigency,
)
from linguoplotter.structures import View
from linguoplotter.structures.links import Relation


class ViewDrivenFactory(Factory):
    """Finds a view with unfilled slots
    and spawns a codelet to suggest a structure that could fill a slot"""

    FLOATING_POINT_TOLERANCE = HyperParameters.FLOATING_POINT_TOLERANCE

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
        self.compatible_sub_views = None

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

    @property
    def target_structures(self) -> StructureCollection:
        return self.bubble_chamber.new_structure_collection(self.target_view)

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
        if self.target_view is None:
            self.target_view = (
                self.bubble_chamber.focus.view
                if self.bubble_chamber.focus.view is not None
                else self.bubble_chamber.production_views.get(key=exigency)
            )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Targeting view {self.target_view}"
        )
        self.target_slot = self._get_target_slot()
        self.bubble_chamber.loggers["activity"].log(
            self, f"Targeting slot {self.target_slot}"
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Slot parent space: {self.target_slot.parent_space}"
        )
        if self.target_slot.parent_space == self.target_view.parent_frame.input_space:
            try:
                follow_up = self._spawn_space_to_frame_correspondence_suggester()
            except MissingStructureError:
                follow_up = self._spawn_non_projection_suggester()
        elif (
            self.target_slot.parent_space == self.target_view.parent_frame.output_space
            or (
                self.target_slot in self.target_view.parent_frame.output_space.contents
                and not self.target_slot.correspondences.is_empty()
            )
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

    def _get_target_slot(self):
        sub_frame_input_structures = (
            self.target_view.parent_frame.input_space.contents.filter(
                lambda x: not x.is_correspondence
                and x.parent_space != self.target_view.parent_frame.input_space
                and x.correspondences.is_empty()
            )
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, sub_frame_input_structures, "sub frame input structures"
        )
        input_structures = self.target_view.parent_frame.input_space.contents.filter(
            lambda x: not x.is_correspondence and x.correspondences.is_empty()
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, input_structures, "input structures"
        )
        output_structures = self.target_view.parent_frame.output_space.contents.filter(
            lambda x: not x.is_correspondence
            and x.parent_space != self.target_view.parent_frame.output_space
            and x.correspondences.is_empty()
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, output_structures, "output structures"
        )
        for structures in [
            sub_frame_input_structures,
            input_structures,
            output_structures,
        ]:
            if not structures.where(is_relation=True).is_empty():
                return structures.where(is_relation=True).get()
            if not structures.where(is_label=True).is_empty():
                return structures.where(is_label=True).get()
            if not structures.where(is_chunk=True).is_empty():
                return structures.where(is_chunk=True).get()

        projectable_structures = (
            self.target_view.parent_frame.output_space.contents.filter(
                lambda x: not x.is_correspondence
                and x.correspondences_to_space(self.target_view.output_space).is_empty()
            )
        )
        if not projectable_structures.where(is_chunk=True).is_empty():
            return projectable_structures.where(is_chunk=True).get()
        if not projectable_structures.where(is_label=True).is_empty():
            return projectable_structures.where(is_label=True).get()
        if not projectable_structures.where(is_relation=True).is_empty():
            return projectable_structures.where(is_relation=True).get()

        raise MissingStructureError

    def _spawn_non_projection_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            self, "Trying to spawn non-projection suggester"
        )
        input_space = self.target_view.input_spaces.get()
        if self.target_slot.is_label:
            if self.target_slot.start.is_label:
                node = (
                    self.target_slot.start.correspondences.filter(
                        lambda x: x.parent_view == self.target_view
                        and x.start.parent_space == input_space
                    )
                    .get()
                    .start
                )
            else:
                node = None
                for node_group in self.target_view.node_groups:
                    if (
                        input_space in node_group
                        and self.target_slot.start in node_group.values()
                    ):
                        node = node_group[input_space]
                        break
                if node is None:
                    if (
                        self.target_slot.start.is_link
                        and self.target_slot.start.is_node
                    ):
                        node = input_space.contents.where(
                            is_labellable=True, is_slot=False
                        ).get(key=labeling_exigency)
                    else:
                        try:
                            node = self.target_view.prioritized_targets.filter(
                                lambda x: x.is_node and not x.is_slot
                            ).get()
                        except MissingStructureError:
                            node = input_space.contents.where(
                                is_node=True, is_slot=False
                            ).get(key=labeling_exigency)
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
            if not self.target_slot.parent_concept.is_slot:
                parent_concept = self.target_slot.parent_concept
            elif self.target_slot.parent_concept.is_filled_in:
                parent_concept = self.target_slot.parent_concept.relatives.where(
                    is_concept=True, is_slot=False
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
                self,
                f"Found parent concept {parent_concept} {parent_concept.structure_type}",
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
                        lambda x: x[0] != x[1]
                        and (
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
                                concept=parent_concept,
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
                self.target_view.unhappiness,
            )
        raise Exception("Slot is not a label or a relation.")

    def _spawn_projection_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            self, "Trying to spawn projection suggester"
        )
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
            self, "Trying to spawn space-to-frame-correspondence suggester"
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
            self.target_view.unhappiness,
        )
        self.bubble_chamber.loggers["activity"].log(self, f"follow_up: {follow_up}")
        follow_up._get_target_conceptual_space(self, follow_up)
        follow_up._get_target_structure_one(self, follow_up)
        return follow_up

    def _spawn_sub_frame_to_frame_correspondence_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            self, "Trying to spawn sub-frame-to-frame-correspondence suggester"
        )
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
            self.target_view.unhappiness,
        )

    def _spawn_potential_sub_frame_to_frame_correspondence_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            self,
            "Trying to spawn potential sub-frame-to-frame-correspondence suggester",
        )
        target_space_two = (
            self.target_view.parent_frame.input_space
            if self.target_slot in self.target_view.parent_frame.input_space.contents
            else self.target_view.parent_frame.output_space
        )
        sub_frame = self.target_view.parent_frame.sub_frames.filter(
            lambda x: x.input_space == self.target_slot.parent_space
            or x.output_space == self.target_slot.parent_space
        ).get()
        self.bubble_chamber.loggers["activity"].log_collection(
            self, self.target_view.node_groups, "node groups"
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, sub_frame.input_space.contents, "sub frame input contents"
        )
        follow_up = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {
                "target_view": self.target_view,
                "target_space_two": target_space_two,
                "target_structure_two": self.target_slot,
                "sub_frame": sub_frame,
            },
            self.target_view.unhappiness,
        )
        follow_up._get_target_conceptual_space(self, follow_up)
        self.compatible_sub_views = self.bubble_chamber.production_views.filter(
            lambda x: (x.parent_frame.parent_concept == sub_frame.parent_concept)
            and (x.input_spaces == self.target_view.input_spaces)
            and all(
                [
                    self.target_view.can_accept_member(
                        member.parent_concept,
                        member.conceptual_space,
                        member.start,
                        member.end,
                    )
                    for member in x.members
                ]
            )
            and (
                (
                    follow_up.target_conceptual_space
                    in x.parent_frame.input_space.conceptual_spaces
                    if self.target_slot.parent_space == sub_frame.input_space
                    else follow_up.target_conceptual_space
                    in x.parent_frame.output_space.conceptual_spaces
                )
                or follow_up.target_conceptual_space is None
            )
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, self.compatible_sub_views, "Compatible sub views"
        )
        views_with_compatible_nodes = self.compatible_sub_views.filter(
            lambda x: x.unhappiness < self.FLOATING_POINT_TOLERANCE
            and any(
                [
                    self.target_view.can_accept_member(
                        member.parent_concept,
                        member.conceptual_space,
                        member.start,
                        self.target_slot,
                    )
                    and self.target_view.can_accept_member(
                        member.parent_concept,
                        member.conceptual_space,
                        member.end,
                        self.target_slot,
                    )
                    for member in x.members.filter(
                        lambda c: type(c.start) == type(self.target_slot)
                        and c.start.parent_space.parent_concept
                        == self.target_slot.parent_space.parent_concept
                    )
                ]
            )
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, views_with_compatible_nodes, "Views with compatible nodes"
        )
        follow_up.target_sub_view = views_with_compatible_nodes.get(key=exigency)
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Found target sub view: {follow_up.target_sub_view}",
        )
        follow_up.target_space_one = (
            follow_up.target_sub_view.parent_frame.input_space
            if follow_up.target_sub_view.parent_frame.input_space.parent_concept
            == target_space_two.parent_concept
            else follow_up.target_sub_view.parent_frame.output_space
        )
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Found target space one: {follow_up.target_space_one}",
        )
        follow_up._get_target_structure_one(self, follow_up)
        return follow_up

    def _spawn_view_driven_factory(self):
        self.bubble_chamber.loggers["activity"].log(
            self,
            "Trying to spawn view-driven factory",
        )
        sub_frame = self.target_view.parent_frame.sub_frames.filter(
            lambda x: x.input_space == self.target_slot.parent_space
            or x.output_space == self.target_slot.parent_space
        ).get()
        contextual_space = self.target_view.input_spaces.get()
        self.compatible_sub_views = self.compatible_sub_views.filter(
            lambda x: x.unhappiness > self.FLOATING_POINT_TOLERANCE
        )
        prioritized_targets = self.bubble_chamber.new_structure_collection(
            *[
                group[contextual_space]
                for node in sub_frame.input_space.contents
                for group in self.target_view.node_groups
                if node in group.values()
            ]
            + [
                correspondence.start
                for correspondence in self.target_view.members
                if correspondence.start.parent_space == contextual_space
            ]
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, prioritized_targets, "prioritized_targets"
        )
        views_with_correct_prioritized_targets = (
            (
                self.compatible_sub_views.filter(
                    lambda x: x.prioritized_targets == prioritized_targets
                )
            )
            if not prioritized_targets.is_empty()
            else self.compatible_sub_views
        )
        self.bubble_chamber.loggers["activity"].log_collection(
            self, self.compatible_sub_views, "Views with correct priotitized_targets"
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
                    in x.parent_frame.output_space.conceptual_spaces
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
            self.target_view.unhappiness,
            target_view=target_sub_view,
        )

    def _spawn_simplex_view_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            self,
            "Trying to spawn simplex view suggester",
        )
        sub_frame = self.target_view.parent_frame.sub_frames.filter(
            lambda x: x.input_space == self.target_slot.parent_space
            or x.output_space == self.target_slot.parent_space
        ).get()
        self.bubble_chamber.loggers["activity"].log(
            self, f"Found sub frame: {sub_frame}"
        )
        contextual_space = self.target_view.input_spaces.get()
        frame = self.bubble_chamber.frames.where(
            is_sub_frame=False, parent_concept=sub_frame.parent_concept
        ).get(key=activation)
        self.bubble_chamber.loggers["activity"].log(
            self, f"Found target frame: {frame}"
        )
        prioritized_targets = self.bubble_chamber.new_structure_collection(
            *[
                group[contextual_space]
                for node in sub_frame.input_space.contents
                for group in self.target_view.node_groups
                if node in group.values()
            ]
            + [
                correspondence.start
                for correspondence in self.target_view.members
                if correspondence.start.parent_space == contextual_space
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
            self.target_view.unhappiness,
        )
