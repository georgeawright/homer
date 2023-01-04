from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Factory
from linguoplotter.codelets.suggesters import (
    LabelSuggester,
    RelationSuggester,
    ViewSuggester,
)
from linguoplotter.codelets.suggesters.correspondence_suggesters import (
    InterspatialCorrespondenceSuggester,
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
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict, StructureSet
from linguoplotter.structure_collection_keys import activation
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
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Factory.__init__(
            self, codelet_id, parent_id, bubble_chamber, coderack, targets, urgency
        )
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
        targets = bubble_chamber.new_dict({"view": target_view}, name="targets")
        return cls(codelet_id, parent_id, bubble_chamber, coderack, targets, urgency)

    def follow_up_urgency(self) -> FloatBetweenOneAndZero:
        if self.bubble_chamber.focus.view is None:
            return self.coderack.MINIMUM_CODELET_URGENCY
        return max(
            1 - self.bubble_chamber.satisfaction, self.coderack.MINIMUM_CODELET_URGENCY
        )

    def _engender_follow_up(self):
        self._set_target_view()
        self._set_target_slot()
        if self.targets["slot"].parent_space is None:
            try:
                follow_up = self._spawn_interspatial_correspondence_suggester()
            except MissingStructureError:
                follow_up = self._spawn_interspatial_relation_suggester()
        elif (
            len(self.targets["slot"].parent_spaces.where(is_contextual_space=True)) == 1
            and self.targets["slot"].parent_space
            == self.targets["view"].parent_frame.input_space
        ):
            try:
                follow_up = self._spawn_space_to_frame_correspondence_suggester()
            except MissingStructureError:
                follow_up = self._spawn_non_projection_suggester()
        elif self.targets["slot"].parent_space == self.targets[
            "view"
        ].parent_frame.output_space or (
            self.targets["slot"]
            in self.targets["view"].parent_frame.output_space.contents
            and self.targets["slot"]
            .correspondences.where(end=self.targets["slot"])
            .not_empty
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
                    follow_up = self._spawn_view_suggester()
        self.child_codelets.append(follow_up)

    def _set_target_view(self):
        if self.bubble_chamber.focus.view is None:
            raise MissingStructureError
        if self.targets["view"] is None:
            self.targets["view"] = self.bubble_chamber.focus.view
        try:
            self.targets["view"] = (
                self.targets["view"].sub_views.filter(lambda x: x.unhappiness > 0).get()
            )
            self._set_target_view()
        except MissingStructureError:
            pass

    def _set_target_slot(self):
        for structures in [
            self.targets["view"].unfilled_interspatial_structures,
            self.targets["view"].unfilled_sub_frame_input_structures,
            self.targets["view"].unfilled_input_structures,
            self.targets["view"].unfilled_output_structures,
        ]:
            if structures.where(is_relation=True).not_empty:
                self.targets["slot"] = structures.where(is_relation=True).get()
                return
        for structures in [
            self.targets["view"].unfilled_interspatial_structures,
            self.targets["view"].unfilled_sub_frame_input_structures,
            self.targets["view"].unfilled_input_structures,
            self.targets["view"].unfilled_output_structures,
        ]:
            if structures.where(is_label=True).not_empty:
                self.targets["slot"] = structures.where(is_label=True).get()
                return
            if structures.where(is_chunk=True).not_empty:
                self.targets["slot"] = structures.where(is_chunk=True).get()
                return
        projectable_structures = self.targets["view"].unfilled_projectable_structures
        if projectable_structures.where(is_chunk=True).not_empty:
            self.targets["slot"] = projectable_structures.where(is_chunk=True).get()
            return
        if projectable_structures.where(is_label=True).not_empty:
            self.targets["slot"] = projectable_structures.where(is_label=True).get()
            return
        if projectable_structures.where(is_relation=True).not_empty:
            self.targets["slot"] = projectable_structures.where(is_relation=True).get()
            return
        raise MissingStructureError

    def _spawn_non_projection_suggester(self):
        self.bubble_chamber.loggers["activity"].log("Spawning non-projection suggester")
        input_space = self.targets["view"].input_spaces.get()
        if self.targets["slot"].is_label:
            possible_nodes = []
            for node_group in self.targets["view"].node_groups:
                if (
                    input_space in node_group
                    and self.targets["slot"].start in node_group.values()
                ):
                    possible_nodes.append(node_group[input_space])
                    break
            if possible_nodes == []:
                possible_nodes = list(
                    input_space.contents.filter(lambda x: x.is_node and x.quality > 0)
                )
            if not self.targets["slot"].parent_concept.is_slot:
                possible_concepts = self.bubble_chamber.new_set(
                    self.targets["slot"].parent_concept
                )
            elif self.targets["slot"].parent_concept.is_filled_in:
                possible_concepts = self.bubble_chamber.new_set(
                    self.targets["slot"].parent_concept.non_slot_value
                )
            elif self.targets["slot"].parent_concept.possible_instances.not_empty:
                possible_concepts = self.targets[
                    "slot"
                ].parent_concept.possible_instances
            elif (
                self.targets["slot"].parent_concept.parent_space.is_slot
                and self.targets[
                    "slot"
                ].parent_concept.parent_space.possible_instances.not_empty
            ):
                possible_concepts = StructureSet.union(
                    *[
                        space.contents.where(is_concept=True, is_slot=False)
                        for space in self.targets[
                            "slot"
                        ].parent_concept.parent_space.possible_instances
                    ]
                )
            else:
                possible_concepts = self.targets[
                    "slot"
                ].parent_concept.parent_space.contents.where(
                    is_concept=True, is_slot=False
                )
            possible_target_combos = [
                self.bubble_chamber.new_dict(
                    {"start": start, "concept": concept}, name="targets"
                )
                for start in possible_nodes
                for concept in possible_concepts
            ]
            targets = self.bubble_chamber.random_machine.select(
                possible_target_combos,
                key=lambda x: x["concept"].classifier.classify(
                    start=x["start"], concept=x["concept"]
                ),
            )
            self.bubble_chamber.loggers["activity"].log_dict(targets)
            return LabelSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                targets,
                targets["concept"].proximity_to(targets["start"])
                if self.targets["slot"].parent_concept.is_slot
                and not self.targets["slot"].parent_concept.is_filled_in
                else self.targets["view"].unhappiness,
            )
        if self.targets["slot"].is_relation:
            target_start = None
            target_end = None
            for node_group in self.targets["view"].node_groups:
                if (
                    input_space in node_group
                    and self.targets["slot"].start in node_group.values()
                ):
                    target_start = node_group[input_space]
                if (
                    input_space in node_group
                    and self.targets["slot"].end in node_group.values()
                ):
                    target_end = node_group[input_space]
            potential_targets = input_space.contents.filter(
                lambda x: x.is_node and not x.is_raw and x.quality > 0
            )
            possible_target_pairs = [
                (a, b)
                for a in potential_targets
                for b in potential_targets
                if a != b
                and (a == target_start if target_start is not None else True)
                and (b == target_end if target_end is not None else True)
            ]
            if not self.targets["slot"].parent_concept.is_slot:
                possible_concepts = [self.targets["slot"].parent_concept]
            elif self.targets["slot"].parent_concept.is_filled_in:
                possible_concepts = [self.targets["slot"].parent_concept.non_slot_value]
            elif self.targets["slot"].parent_concept.possible_instances.not_empty:
                possible_concepts = list(
                    self.targets["slot"].parent_concept.possible_instances
                )
            else:
                possible_concepts = [
                    concept
                    for space in self.targets["slot"].parent_spaces.filter(
                        lambda x: x.is_conceptual_space
                        and x.parent_concept.structure_type == Relation
                    )
                    for concept in space.contents.where(is_concept=True, is_slot=False)
                ]
            if not self.targets["slot"].conceptual_space.is_slot:
                possible_spaces = [self.targets["slot"].conceptual_space]
            else:
                possible_spaces = list(
                    self.targets["slot"].conceptual_space.possible_instances.filter(
                        lambda x: x
                        in self.targets["view"]
                        .input_spaces.get()
                        .conceptual_spaces_and_sub_spaces
                    )
                )
            possible_target_combos = [
                self.bubble_chamber.new_dict(
                    {"start": start, "end": end, "space": space, "concept": concept},
                    name="targets",
                )
                for start, end in possible_target_pairs
                for space in possible_spaces
                for concept in possible_concepts
            ]
            targets = self.bubble_chamber.random_machine.select(
                possible_target_combos,
                key=lambda x: x["concept"].classifier.classify(
                    start=x["start"],
                    end=x["end"],
                    concept=x["concept"],
                    space=x["space"],
                ),
            )
            self.bubble_chamber.loggers["activity"].log_dict(targets)
            return RelationSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                targets,
                targets["concept"].classifier.classify(
                    start=targets["start"],
                    end=targets["end"],
                    concept=targets["concept"],
                    space=targets["space"],
                )
                if self.targets["slot"].parent_concept.is_slot
                and not self.targets["slot"].parent_concept.is_filled_in
                else self.targets["view"].unhappiness,
            )
        raise Exception("Slot is not a label or a relation.")

    def _spawn_interspatial_relation_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            "Spawning interspatial relation suggester"
        )
        target_start = None
        target_end = None
        for node_group in self.targets["view"].node_groups:
            if None in node_group and self.targets["slot"].start in node_group.values():
                target_start = node_group[None]
            if None in node_group and self.targets["slot"].end in node_group.values():
                target_end = node_group[None]
        for sub_frame in self.targets["view"].parent_frame.sub_frames:
            if (
                self.targets["slot"].start in sub_frame.input_space.contents
                or self.targets["slot"].start in sub_frame.input_space.contents
            ):
                start_sub_frame = sub_frame
            if (
                self.targets["slot"].end in sub_frame.input_space.contents
                or self.targets["slot"].end in sub_frame.input_space.contents
            ):
                end_sub_frame = sub_frame
        potential_start_views = self.bubble_chamber.views.filter(
            lambda x: x.parent_frame.parent_concept == start_sub_frame.parent_concept
        )
        potential_start_views = potential_start_views.sample(
            len(potential_start_views) // 2
        )
        potential_start_targets = self.bubble_chamber.new_set(
            *[
                view.early_chunk
                if self.targets["slot"].start == start_sub_frame.early_chunk
                else view.late_chunk
                for view in potential_start_views
                if not view.early_chunk.is_slot or view.early_chunk.is_filled_in
            ]
        )
        potential_end_views = self.bubble_chamber.views.filter(
            lambda x: x.parent_frame.parent_concept == end_sub_frame.parent_concept
            and x not in potential_start_views
        )
        potential_end_targets = self.bubble_chamber.new_set(
            *[
                view.early_chunk
                if self.targets["slot"].end == end_sub_frame.early_chunk
                else view.late_chunk
                for view in potential_end_views
                if not view.late_chunk.is_slot or view.late_chunk.is_filled_in
            ]
        )
        # TODO: prioritise completed views
        possible_target_pairs = [
            (a, b)
            for a in potential_start_targets
            for b in potential_end_targets
            if a != b
            and (a == target_start if target_start is not None else True)
            and (b == target_end if target_end is not None else True)
        ]
        if not self.targets["slot"].parent_concept.is_slot:
            possible_concepts = [self.targets["slot"].parent_concept]
        elif self.targets["slot"].parent_concept.is_filled_in:
            possible_concepts = [self.targets["slot"].parent_concept.non_slot_value]
        elif self.targets["slot"].parent_concept.possible_instances.not_empty:
            possible_concepts = list(
                self.targets["slot"].parent_concept.possible_instances
            )
        else:
            possible_concepts = [
                concept
                for space in self.targets["slot"].parent_spaces.filter(
                    lambda x: x.is_conceptual_space
                    and x.parent_concept.structure_type == Relation
                )
                for concept in space.contents.where(is_concept=True, is_slot=False)
            ]
        if not self.targets["slot"].conceptual_space.is_slot:
            possible_spaces = [self.targets["slot"].conceptual_space]
        else:
            possible_spaces = list(
                self.targets["slot"].conceptual_space.possible_instances.filter(
                    lambda x: x
                    in self.targets["view"]
                    .input_spaces.get()
                    .conceptual_spaces_and_sub_spaces
                )
            )
        possible_target_combos = [
            self.bubble_chamber.new_dict(
                {"start": start, "end": end, "space": space, "concept": concept},
                name="targets",
            )
            for start, end in possible_target_pairs
            for space in possible_spaces
            for concept in possible_concepts
        ]
        targets = self.bubble_chamber.random_machine.select(
            possible_target_combos,
            key=lambda x: x["concept"].classifier.classify(
                start=x["start"].non_slot_value if x["start"].is_slot else x["start"],
                end=x["end"].non_slot_value if x["end"].is_slot else x["end"],
                concept=x["concept"],
                space=x["space"],
            ),
        )
        self.bubble_chamber.loggers["activity"].log_dict(targets)
        return RelationSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            targets,
            targets["concept"].classifier.classify(
                start=targets["start"].non_slot_value
                if targets["start"].is_slot
                else targets["start"],
                end=targets["end"].non_slot_value
                if targets["end"].is_slot
                else targets["end"],
                concept=targets["concept"],
                space=targets["space"],
            )
            if self.targets["slot"].parent_concept.is_slot
            and not self.targets["slot"].parent_concept.is_filled_in
            else self.targets["view"].unhappiness,
        )

    def _spawn_projection_suggester(self):
        self.bubble_chamber.loggers["activity"].log("Spawning ProjectionSuggester")
        if self.targets["slot"].is_letter_chunk:
            follow_up_class = LetterChunkProjectionSuggester
        elif self.targets["slot"].is_chunk:
            follow_up_class = ChunkProjectionSuggester
        elif self.targets["slot"].is_label:
            follow_up_class = LabelProjectionSuggester
        elif self.targets["slot"].is_relation:
            follow_up_class = RelationProjectionSuggester
        targets = self.bubble_chamber.new_dict(
            {"view": self.targets["view"], "projectee": self.targets["slot"]},
            name="targets",
        )
        return follow_up_class.spawn(
            self.codelet_id,
            self.bubble_chamber,
            targets,
            self.targets["slot"].uncorrespondedness
            if not self.targets["slot"].is_chunk
            else 1.0,
        )

    def _spawn_interspatial_correspondence_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            "Spawning InterspatialCorrespondenceSuggester"
        )
        targets = self.bubble_chamber.new_dict(
            {
                "view": self.targets["view"],
                "end": self.targets["slot"],
                "concept": self.bubble_chamber.concepts["same"],
            },
            name="targets",
        )
        follow_up = InterspatialCorrespondenceSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            targets,
            self.targets["view"].unhappiness,
        )
        follow_up._get_target_conceptual_space(self, follow_up)
        follow_up._get_target_structure_one(self, follow_up)
        return follow_up

    def _spawn_space_to_frame_correspondence_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            "Spawning SpaceToFrameCorrespondenceSuggester"
        )
        targets = self.bubble_chamber.new_dict(
            {
                "view": self.targets["view"],
                "end": self.targets["slot"],
                "concept": self.bubble_chamber.concepts["same"],
            },
            name="targets",
        )
        follow_up = SpaceToFrameCorrespondenceSuggester.spawn(
            self.codelet_id,
            self.bubble_chamber,
            targets,
            self.targets["view"].unhappiness,
        )
        follow_up._get_target_conceptual_space(self, follow_up)
        follow_up._get_target_structure_one(self, follow_up)
        return follow_up

    def _spawn_sub_frame_to_frame_correspondence_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            "Spawning SubFrameToFrameCorrespondenceSuggester"
        )
        targets = self.bubble_chamber.new_dict(
            {"view": self.targets["view"], "end": self.targets["slot"]}, name="targets"
        )
        targets["end_space"] = (
            targets["view"].parent_frame.input_space
            if targets["end"] in targets["view"].parent_frame.input_space.contents
            else targets["view"].parent_frame.output_space
        )
        targets["sub_frame"] = (
            targets["view"]
            .parent_frame.sub_frames.filter(
                lambda x: (
                    x.input_space in targets["end"].parent_spaces
                    or x.output_space in targets["end"].parent_spaces
                )
                and not targets["end"].has_correspondence_to_space(
                    targets["view"].matched_sub_frames[x].input_space
                )
                if x in targets["view"].matched_sub_frames
                else False
                and not targets["end"].has_correspondence_to_space(
                    targets["view"].matched_sub_frames[x].output_space
                )
                if x in targets["view"].matched_sub_frames
                else False
            )
            .get()
        )
        if targets["sub_frame"] not in targets["view"].matched_sub_frames:
            raise MissingStructureError
        matching_frame = targets["view"].matched_sub_frames[targets["sub_frame"]]
        targets["start_space"] = (
            matching_frame.input_space
            if targets["end_space"] == targets["view"].parent_frame.input_space
            else matching_frame.output_space
        )
        follow_up = SubFrameToFrameCorrespondenceSuggester.spawn(
            self.codelet_id, self.bubble_chamber, targets, targets["view"].unhappiness
        )
        follow_up._get_target_conceptual_space(self, follow_up)
        follow_up._get_target_structure_one(self, follow_up)
        return follow_up

    def _spawn_potential_sub_frame_to_frame_correspondence_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            "Spawning PotentialSubFrameToFrameCorrespondenceSuggester"
        )
        targets = self.bubble_chamber.new_dict(
            {"view": self.targets["view"], "end": self.targets["slot"]}, name="targets"
        )
        targets["end_space"] = (
            targets["view"].parent_frame.input_space
            if targets["end"] in targets["view"].parent_frame.input_space.contents
            else targets["view"].parent_frame.output_space
        )
        targets["sub_frame"] = (
            targets["view"]
            .parent_frame.sub_frames.filter(
                lambda x: x not in targets["view"].matched_sub_frames
                and (
                    x.input_space in targets["end"].parent_spaces
                    or x.output_space in targets["end"].parent_spaces
                )
            )
            .get()
        )
        targets["concept"] = self.bubble_chamber.concepts["same"]
        follow_up = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
            self.codelet_id, self.bubble_chamber, targets, targets["view"].unhappiness
        )
        follow_up._get_target_conceptual_space(self, follow_up)
        follow_up._get_target_space_one(self, follow_up)
        follow_up._get_target_structure_one(self, follow_up)
        return follow_up

    def _spawn_view_suggester(self):
        self.bubble_chamber.loggers["activity"].log("Spawning ViewSuggester")
        sub_frame = (
            self.targets["view"]
            .parent_frame.sub_frames.filter(
                lambda x: x.input_space in self.targets["slot"].parent_spaces
                or x.output_space in self.targets["slot"].parent_spaces
            )
            .get()
        )
        self.bubble_chamber.loggers["activity"].log(f"Found sub frame: {sub_frame}")
        frame = self.bubble_chamber.frames.where(
            is_sub_frame=False, parent_concept=sub_frame.parent_concept
        ).get(key=activation)
        self.bubble_chamber.loggers["activity"].log(f"Found target frame: {frame}")
        urgency = self.targets["view"].unhappiness
        return ViewSuggester.make(
            self.codelet_id, self.bubble_chamber, frame=frame, urgency=urgency
        )
