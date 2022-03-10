import statistics

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
from homer.structure import Structure
from homer.structure_collection_keys import (
    activation,
    exigency,
    labeling_exigency,
    uncorrespondedness,
)
from homer.structures import View


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
    ):
        Factory.__init__(self, codelet_id, parent_id, bubble_chamber, coderack, urgency)

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
        view = (
            self.bubble_chamber.focus.view
            if self.bubble_chamber.focus.view is not None
            else self.bubble_chamber.production_views.get(key=exigency)
        )
        self.bubble_chamber.loggers["activity"].log(self, f"Targeting view {view}")
        input_structures = view.parent_frame.input_space.contents.filter(
            lambda x: not x.is_correspondence and x.correspondences.is_empty()
        )
        try:
            slot = input_structures.get(key=uncorrespondedness)
        except MissingStructureError:
            output_structures = view.parent_frame.output_space.contents.filter(
                lambda x: not x.is_correspondence and x.correspondences.is_empty()
            )
            self.bubble_chamber.loggers["activity"].log_collection(
                self, output_structures, "Uncorrespondended output structures"
            )
            slot = output_structures.get(key=uncorrespondedness)
        self.bubble_chamber.loggers["activity"].log(self, f"Targeting slot {slot}")
        if slot.parent_space == view.parent_frame.input_space:
            try:
                follow_up = self._spawn_space_to_frame_correspondence_suggester(
                    view, slot
                )
            except MissingStructureError:
                follow_up = self._spawn_non_projection_suggester(view, slot)
        elif slot.parent_space == view.parent_frame.output_space:
            follow_up = self._spawn_projection_suggester(view, slot)
        else:  # slot is in sub-frame
            try:
                follow_up = self._spawn_sub_frame_to_frame_correspondence_suggester(
                    view, slot
                )
            except MissingStructureError:
                try:
                    follow_up = self._spawn_potential_sub_frame_to_frame_correspondence_suggester(
                        view, slot
                    )
                except MissingStructureError:
                    follow_up = self._spawn_simplex_view_suggester(view, slot)
        self.child_codelets.append(follow_up)

    def _spawn_non_projection_suggester(self, view: View, slot: Structure):
        input_space = view.input_spaces.get()
        if slot.is_label:
            node = None
            for node_group in view.node_groups:
                if input_space in node_group and slot.start in node_group.values():
                    node = node_group[input_space]
                    break
            if node is None:
                if slot.is_link and slot.is_node:
                    node = input_space.contents.where(
                        is_labellable=True, is_slot=False
                    ).get(key=labeling_exigency)
                else:
                    node = input_space.contents.where(is_node=True, is_slot=False).get(
                        key=labeling_exigency
                    )
            parent_concept = (
                slot.parent_spaces.where(is_conceptual_space=True)
                .get()
                .contents.where(is_concept=True, is_slot=False)
                .get(key=lambda x: x.proximity_to(node))
            )
            return LabelSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {"target_node": node, "parent_concept": parent_concept},
                slot.uncorrespondedness,
            )
        if slot.is_relation:
            if slot.parent_concept.is_filled_in:
                parent_concept = slot.parent_concept.relatives.where(
                    is_slot=False
                ).get()
            else:
                parent_concept = (
                    slot.parent_spaces.where(is_conceptual_space=True)
                    .get()
                    .contents.where(is_concept=True, is_slot=False)
                    .get(key=activation)
                )
            potential_targets = input_space.contents.where(is_node=True, is_slot=False)
            try:
                (
                    target_structure_one,
                    target_structure_two,
                ) = potential_targets.pairs.get(
                    key=lambda x: parent_concept.classifier.classify(
                        start=x[0], end=x[1], space=slot.conceptual_space
                    )
                )
            except NoLocationError:
                raise MissingStructureError
            return RelationSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "target_space": slot.conceptual_space,
                    "target_structure_one": target_structure_one,
                    "target_structure_two": target_structure_two,
                    "parent_concept": parent_concept,
                },
                slot.uncorrespondedness,
            )
        raise Exception("Slot is not a label or a relation.")

    def _spawn_projection_suggester(self, view: View, slot: Structure):
        if slot.is_letter_chunk:
            follow_up_class = LetterChunkProjectionSuggester
        elif slot.is_chunk:
            follow_up_class = ChunkProjectionSuggester
        elif slot.is_label:
            follow_up_class = LabelProjectionSuggester
        elif slot.is_relation:
            follow_up_class = RelationProjectionSuggester
        return follow_up_class.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {"target_view": view, "target_projectee": slot},
            slot.uncorrespondedness,
        )

    def _spawn_space_to_frame_correspondence_suggester(
        self, view: View, slot: Structure
    ):
        self.bubble_chamber.loggers["activity"].log(
            self, "Trying to build correspondence suggester"
        )
        target_conceptual_space = (
            None if slot.is_chunk else slot.parent_concept.parent_space
        )
        follow_up = SpaceToFrameCorrespondenceSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {
                "target_view": view,
                "target_space_one": view.input_spaces.get(),
                "target_space_two": view.parent_frame.input_space,
                "target_structure_two": slot,
                "target_conceptual_space": target_conceptual_space,
                "parent_concept": self.bubble_chamber.concepts["same"],
            },
            slot.uncorrespondedness,
        )
        self.bubble_chamber.loggers["activity"].log(self, f"follow_up: {follow_up}")
        follow_up._get_target_structure_one(self, follow_up)
        return follow_up

    def _spawn_sub_frame_to_frame_correspondence_suggester(
        self, view: View, slot: Structure
    ):
        target_space_two = (
            view.parent_frame.input_space
            if slot in view.parent_frame.input_space.contents
            else view.parent_frame.output_space
        )
        if target_space_two not in view.matched_sub_frames.keys():
            raise MissingStructureError
        return SubFrameToFrameCorrespondenceSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {
                "target_view": view,
                "target_space_two": target_space_two,
                "target_structure_two": slot,
            },
            slot.uncorrespondedness,
        )

    def _spawn_potential_sub_frame_to_frame_correspondence_suggester(
        self, view: View, slot: Structure
    ):
        target_space_two = (
            view.parent_frame.input_space
            if slot in view.parent_frame.input_space.contents
            else view.parent_frame.output_space
        )
        sub_frame = view.parent_frame.sub_frames.filter(
            lambda x: x.input_space == slot.parent_space
            or x.output_space == slot.parent_space
        ).get()
        if self.bubble_chamber.production_views.filter(
            lambda x: x.parent_frame.parent_concept == sub_frame.parent_concept
        ).is_empty():
            raise MissingStructureError
        return PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {
                "target_view": view,
                "target_space_two": target_space_two,
                "target_structure_two": slot,
                "sub_frame": sub_frame,
            },
            slot.uncorrespondedness,
        )

    def _spawn_simplex_view_suggester(self, view: View, slot: Structure):
        sub_frame = view.parent_frame.sub_frames.filter(
            lambda x: x.input_space == slot.parent_space
            or x.output_space == slot.parent_space
        ).get()
        contextual_space = view.input_spaces.get()
        frame = self.bubble_chamber.frames.where(
            is_sub_frame=False, parent_concept=sub_frame.parent_concept
        ).get(key=activation)
        return SimplexViewSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            {"frame": frame, "contextual_space": contextual_space},
            slot.uncorrespondedness,
        )
