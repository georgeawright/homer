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
from linguoplotter.codelets.suggesters.label_suggesters import (
    InterspatialLabelSuggester,
)
from linguoplotter.codelets.suggesters.relation_suggesters import (
    InterspatialRelationSuggester,
)
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict, StructureSet
from linguoplotter.structure_collection_keys import activation
from linguoplotter.structures import View
from linguoplotter.structures.links import Relation


class ViewDrivenFactory(Factory):
    """
    Finds an unfilled slot in the focus frame
    spawns a suggester codelet that targets the slot"""

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

    @property
    def follow_up_urgency(self) -> FloatBetweenOneAndZero:
        if self.bubble_chamber.focus.view is None:
            return self.coderack.MINIMUM_CODELET_URGENCY
        return max(
            1 - self.bubble_chamber.satisfaction, self.coderack.MINIMUM_CODELET_URGENCY
        )

    def _engender_follow_up(self):
        self._set_target_view()
        if self.targets["frame"].has_failed_to_match:
            return
        self._set_target_slot()
        if self.targets["slot"].is_interspatial:
            try:
                follow_up = self._spawn_interspatial_correspondence_suggester()
            except MissingStructureError:
                follow_up = self._spawn_interspatial_link_suggester()
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
            "frame"
        ].output_space or (
            self.targets["slot"] in self.targets["frame"].output_space.contents
            and self.targets["slot"]
            .correspondences.where(end=self.targets["slot"])
            .not_empty
        ):
            follow_up = self._spawn_projection_suggester()
        else:
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
            self.targets["frame"] = self.targets["view"].parent_frame

    def _set_target_slot(self):
        interspatial_structures = self.targets["frame"].unfilled_interspatial_structures
        if interspatial_structures.not_empty:
            if interspatial_structures.where(is_label=True).not_empty:
                self.targets["slot"] = interspatial_structures.where(
                    is_label=True
                ).get()
            else:
                self.targets["slot"] = interspatial_structures.get()
            return
        if self.targets["frame"].unfilled_interspatial_structures.not_empty:
            self.targets["frame"].unfilled_interspatial_structures.get()
            return
        for structures in [
            self.targets["frame"].unfilled_sub_frame_input_structures,
            self.targets["frame"].unfilled_input_structures,
            self.targets["frame"].unfilled_output_structures,
        ]:
            if structures.where(is_relation=True).not_empty:
                self.targets["slot"] = structures.where(is_relation=True).get()
                return
        for structures in [
            self.targets["frame"].unfilled_sub_frame_input_structures,
            self.targets["frame"].unfilled_input_structures,
            self.targets["frame"].unfilled_output_structures,
        ]:
            if structures.where(is_label=True).not_empty:
                self.targets["slot"] = structures.where(is_label=True).get()
                return
            if structures.where(is_chunk=True).not_empty:
                self.targets["slot"] = structures.where(is_chunk=True).get()
                return
        projectable_structures = self.targets["frame"].unfilled_projectable_structures
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
                        space.contents.filter(
                            lambda x: x.is_concept
                            and not x.is_slot
                            and (
                                not x.is_compound_concept or x.args[0].is_fully_active()
                            )
                        )
                        for space in self.targets[
                            "slot"
                        ].parent_concept.parent_space.possible_instances
                    ]
                )
            else:
                possible_concepts = self.targets[
                    "slot"
                ].parent_concept.parent_space.contents.filter(
                    lambda x: x.is_concept
                    and not x.is_slot
                    and (not x.is_compound_concept or x.args[0].is_fully_active())
                )
            possible_target_combos = [
                self.bubble_chamber.new_dict(
                    {"start": start, "concept": concept}, name="targets"
                )
                for start in possible_nodes
                for concept in possible_concepts
                if start.labels.where(parent_concept=concept).is_empty
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
            if target_start is not None and target_end is not None:
                possible_target_pairs = [(target_start, target_end)]
            else:
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
                    for concept in space.contents.filter(
                        lambda x: x.is_concept
                        and not x.is_slot
                        and (not x.is_compound_concept or x.args[0].is_fully_active())
                    )
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
                if start.relations.filter(
                    lambda x: x.end == end
                    and x.conceptual_space == space
                    and x.parent_concept == concept
                    and x.activation > 0
                ).is_empty
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

    def _spawn_interspatial_link_suggester(self):
        self.bubble_chamber.loggers["activity"].log(
            "Spawning interspatial link suggester"
        )
        if self.targets["slot"].is_relation:
            target_start_space = None
            target_end_space = None
            for link in self.targets["frame"].interspatial_links:
                for correspondee in link.correspondees:
                    if (
                        link.start.parent_space
                        == self.targets["slot"].start.parent_space
                    ):
                        target_start_space = correspondee.start.parent_space
                    if (
                        link.is_relation
                        and link.end.parent_space
                        == self.targets["slot"].start.parent_space
                    ):
                        target_start_space = correspondee.end.parent_space
                    if link.start.parent_space == self.targets["slot"].end.parent_space:
                        target_end_space = correspondee.start.parent_space
                    if (
                        link.is_relation
                        and link.end.parent_space
                        == self.targets["slot"].end.parent_space
                    ):
                        target_end_space = correspondee.end.parent_space
            for sub_frame in self.targets["frame"].sub_frames:
                if (
                    self.targets["slot"].start in sub_frame.input_space.contents
                    or self.targets["slot"].start in sub_frame.output_space.contents
                ):
                    start_sub_frame = sub_frame
                if (
                    self.targets["slot"].end in sub_frame.input_space.contents
                    or self.targets["slot"].end in sub_frame.output_space.contents
                ):
                    end_sub_frame = sub_frame
            if target_start_space is None:
                potential_start_views = self.bubble_chamber.views.filter(
                    lambda x: x.parent_frame.parent_concept
                    == start_sub_frame.parent_concept
                    and x.unhappiness < self.FLOATING_POINT_TOLERANCE
                )
                potential_start_targets = StructureSet.union(
                    *[
                        view.output_space.contents.filter(
                            lambda x: x.is_chunk
                            and x.members.is_empty
                            and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
                        )
                        if self.targets["slot"].start
                        in self.targets["frame"].output_space.contents
                        else view.parent_frame.input_space.contents.filter(
                            lambda x: x.is_chunk and (not x.is_slot or x.is_filled_in)
                        )
                        for view in potential_start_views
                    ]
                )
            else:
                potential_start_views = self.bubble_chamber.views.filter(
                    lambda x: target_start_space
                    in [x.parent_frame.input_space, x.output_space]
                )
                if self.targets["slot"].start in self.targets["view"].grouped_nodes:
                    start_node_group = [
                        group
                        for group in self.targets["view"].node_groups
                        if self.targets["slot"].start in group.values()
                    ][0]
                    try:
                        structure_one_start = start_node_group[target_start_space]
                        self.bubble_chamber.loggers["activity"].log(
                            f"Found structure one start: {structure_one_start}"
                        )
                    except KeyError:
                        self.bubble_chamber.loggers["activity"].log(
                            "Start node group has no member in target space one"
                        )
                        structure_one_start = None
                else:
                    self.bubble_chamber.loggers["activity"].log(
                        "Structure two start not in grouped nodes"
                    )
                    structure_one_start = None
                if structure_one_start is not None:
                    potential_start_targets = [structure_one_start]
                else:
                    potential_start_targets = StructureSet.union(
                        *[
                            view.output_space.contents.filter(
                                lambda x: x.is_chunk and x.members.is_empty
                            )
                            if self.targets["slot"].start
                            in self.targets["frame"].output_space.contents
                            else view.parent_frame.input_space.contents.filter(
                                lambda x: x.is_chunk
                                and (not x.is_slot or x.is_filled_in)
                            )
                            for view in potential_start_views
                        ]
                    )
            if target_end_space is None:
                potential_end_views = self.bubble_chamber.views.filter(
                    lambda x: x.parent_frame.parent_concept
                    == end_sub_frame.parent_concept
                    and x.unhappiness < self.FLOATING_POINT_TOLERANCE
                )
                if potential_end_views.is_empty:
                    raise MissingStructureError
                potential_end_targets = StructureSet.union(
                    *[
                        view.output_space.contents.filter(
                            lambda x: x.is_chunk
                            and x.members.is_empty
                            and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
                        )
                        if self.targets["slot"].end
                        in self.targets["frame"].output_space.contents
                        else view.parent_frame.input_space.contents.filter(
                            lambda x: x.is_chunk and (not x.is_slot or x.is_filled_in)
                        )
                        for view in potential_end_views
                    ]
                )
            else:
                potential_end_views = self.bubble_chamber.views.filter(
                    lambda x: target_end_space
                    in [x.parent_frame.input_space, x.output_space]
                )
                if self.targets["slot"].end in self.targets["view"].grouped_nodes:
                    end_node_group = [
                        group
                        for group in self.targets["view"].node_groups
                        if self.targets["slot"].end in group.values()
                    ][0]
                    try:
                        structure_one_end = end_node_group[target_end_space]
                        self.bubble_chamber.loggers["activity"].log(
                            f"Found structure one end: {structure_one_end}"
                        )
                    except KeyError:
                        self.bubble_chamber.loggers["activity"].log(
                            "End node group has no member in target space one"
                        )
                        structure_one_end = None
                else:
                    self.bubble_chamber.loggers["activity"].log(
                        "Structure two end not in grouped nodes"
                    )
                    structure_one_end = None
                if structure_one_end is not None:
                    potential_end_targets = [structure_one_end]
                else:
                    potential_end_targets = StructureSet.union(
                        *[
                            view.output_space.contents.filter(
                                lambda x: x.is_chunk and x.members.is_empty
                            )
                            if self.targets["slot"].end
                            in self.targets["frame"].output_space.contents
                            else view.parent_frame.input_space.contents.filter(
                                lambda x: x.is_chunk
                                and (not x.is_slot or x.is_filled_in)
                            )
                            for view in potential_end_views
                        ]
                    )
            possible_target_pairs = [
                (a, b)
                for a in potential_start_targets
                for b in potential_end_targets
                if a != b and a.parent_space != b.parent_space
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
                if start.has_location_in_space(space)
                and end.has_location_in_space(space)
                and space in start.parent_space.conceptual_spaces
            ]
            targets = self.bubble_chamber.random_machine.select(
                possible_target_combos,
                key=lambda x: x["concept"].classifier.classify(
                    start=x["start"].non_slot_value
                    if x["start"].is_slot
                    else x["start"],
                    end=x["end"].non_slot_value if x["end"].is_slot else x["end"],
                    concept=x["concept"],
                    space=x["space"],
                ),
            )
            self.bubble_chamber.loggers["activity"].log_dict(targets)
            return InterspatialRelationSuggester.spawn(
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
                else self.bubble_chamber.focus.unhappiness,
            )
        elif self.targets["slot"].is_label:
            target_start_space = None
            for link in self.targets["frame"].interspatial_links:
                for correspondee in link.correspondees:
                    if (
                        link.start.parent_space
                        == self.targets["slot"].start.parent_space
                    ):
                        target_start_space = correspondee.start.parent_space
                    if (
                        link.is_relation
                        and link.end.parent_space
                        == self.targets["slot"].start.parent_space
                    ):
                        target_start_space = correspondee.end.parent_space
            for sub_frame in self.targets["frame"].sub_frames:
                if (
                    self.targets["slot"].start in sub_frame.input_space.contents
                    or self.targets["slot"].start in sub_frame.output_space.contents
                ):
                    start_sub_frame = sub_frame
            if target_start_space is None:
                potential_start_views = self.bubble_chamber.views.filter(
                    lambda x: x.parent_frame.parent_concept
                    == start_sub_frame.parent_concept
                    and x.parent_frame
                    not in self.targets["view"].matched_sub_frames.values()
                    and x.unhappiness < self.FLOATING_POINT_TOLERANCE
                    and not any(
                        [
                            x.raw_input_nodes == sub_view.raw_input_nodes
                            for sub_view in self.targets["view"].sub_views
                        ]
                    )
                )
            else:
                potential_start_views = self.bubble_chamber.views.filter(
                    lambda x: target_start_space
                    in [x.parent_frame.input_space, x.output_space]
                )
            if potential_start_views.is_empty:
                raise MissingStructureError
            potential_start_targets = StructureSet.union(
                *[
                    view.output_space.contents.filter(
                        lambda x: x.is_chunk
                        and x.members.is_empty
                        and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
                    )
                    if self.targets["slot"].start
                    in self.targets["frame"].output_space.contents
                    else view.parent_frame.input_space.contents.filter(
                        lambda x: x.is_chunk and (not x.is_slot or x.is_filled_in)
                    )
                    for view in potential_start_views
                ]
            )
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
            if (
                not self.targets["slot"]
                .parent_spaces.where(is_conceptual_space=True)
                .get()
                .is_slot
            ):
                possible_spaces = [
                    self.targets["slot"]
                    .parent_spaces.where(is_conceptual_space=True)
                    .get()
                ]
            else:
                possible_spaces = list(
                    self.targets["slot"]
                    .parent_spaces.where(is_conceptual_space=True)
                    .get()
                    .possible_instances.filter(
                        lambda x: x
                        in self.targets["view"]
                        .input_spaces.get()
                        .conceptual_spaces_and_sub_spaces
                    )
                )
            possible_target_combos = [
                self.bubble_chamber.new_dict(
                    {"start": start, "space": space, "concept": concept},
                    name="targets",
                )
                for start in potential_start_targets
                for space in possible_spaces
                for concept in possible_concepts
                if start.has_location_in_space(space)
                and space in start.parent_space.conceptual_spaces
            ]
            targets = self.bubble_chamber.random_machine.select(
                possible_target_combos,
                key=lambda x: x["concept"].classifier.classify(
                    start=x["start"].non_slot_value
                    if x["start"].is_slot
                    else x["start"],
                    concept=x["concept"],
                    space=x["space"],
                ),
            )
            self.bubble_chamber.loggers["activity"].log_dict(targets)
            return InterspatialLabelSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                targets,
                targets["concept"].classifier.classify(
                    start=targets["start"].non_slot_value
                    if targets["start"].is_slot
                    else targets["start"],
                    concept=targets["concept"],
                    space=targets["space"],
                )
                if self.targets["slot"].parent_concept.is_slot
                and not self.targets["slot"].parent_concept.is_filled_in
                else self.bubble_chamber.focus.unhappiness,
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
            {
                "view": self.targets["view"],
                "frame": self.targets["frame"],
                "projectee": self.targets["slot"],
            },
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
                "frame": self.targets["frame"],
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
                "frame": self.targets["frame"],
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
            {
                "view": self.targets["view"],
                "frame": self.targets["frame"],
                "end": self.targets["slot"],
            },
            name="targets",
        )
        targets["end_space"] = (
            targets["view"].parent_frame.input_space
            if targets["end"] in targets["view"].parent_frame.input_space.contents
            else targets["view"].parent_frame.output_space
        )
        targets["sub_frame"] = (
            targets["frame"]
            .sub_frames.filter(
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
            {
                "view": self.targets["view"],
                "frame": self.targets["frame"],
                "end": self.targets["slot"],
            },
            name="targets",
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
            is_sub_frame=False,
            parent_concept=sub_frame.parent_concept,
        ).get(key=activation)
        self.bubble_chamber.loggers["activity"].log(f"Found target frame: {frame}")
        urgency = self.targets["view"].unhappiness
        return ViewSuggester.make(
            self.codelet_id, self.bubble_chamber, frame=frame, urgency=urgency
        )
