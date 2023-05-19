from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection_keys import (
    activation,
    exigency,
    uncorrespondedness,
)
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures.nodes import Concept


class InterspatialCorrespondenceSuggester(CorrespondenceSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.correspondence_builders import (
            InterspatialCorrespondenceBuilder,
        )

        return InterspatialCorrespondenceBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.views.get(key=exigency)
        end = target_view.unfilled_interspatial_structures.get(key=uncorrespondedness)
        urgency = urgency if urgency is not None else end.uncorrespondedness
        targets = bubble_chamber.new_dict(
            {"target_view": target_view, "end": end}, name="targets"
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.views.get(key=activation)
        end = target_view.unfilled_interspatial_structures.get(key=uncorrespondedness)
        urgency = urgency if urgency is not None else end.uncorrespondedness
        targets = bubble_chamber.new_dict(
            {"target_view": target_view, "end": end, "concept": concept},
            name="targets",
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            urgency,
        )

    def _passes_preliminary_checks(self):
        self._get_target_conceptual_space(self, self)
        if (
            self.targets["start"] is not None
            and self.targets["concept"] is not None
            and not (
                self.targets["view"].members.is_empty
                and self.targets["view"].super_views.is_empty
            )
        ):
            if self.targets["space"] is not None and self.targets["space"].is_slot:
                if self.targets["start"].is_label:
                    classification_space = (
                        self.targets["start"]
                        .parent_spaces.where(is_conceptual_space=True)
                        .get()
                    )
                else:
                    classification_space = self.targets["start"].conceptual_space
            else:
                classification_space = self.targets["space"]
            classification = self.targets["concept"].classifier.classify(
                concept=self.targets["concept"],
                space=classification_space,
                start=self.targets["start"],
                end=self.targets["end"],
                view=self.targets["view"],
            )
            self.bubble_chamber.loggers["activity"].log(
                f"Preliminary classification: {classification}"
            )
            if classification < 0.5:
                self.targets["concept"] = self.bubble_chamber.new_compound_concept(
                    self.bubble_chamber.concepts["not"], [self.targets["concept"]]
                )
        else:
            self.targets["concept"] = self.bubble_chamber.concepts["same"]
        try:
            if self.targets["start"] is None:
                self._get_target_structure_one(self, self)
        except MissingStructureError:
            self.bubble_chamber.loggers["activity"].log(
                "MissingStructureError when searching for input target space and structure",
            )
            return False
        if not self.targets["view"].can_accept_member(
            self.targets["concept"],
            self.targets["space"],
            self.targets["start"],
            self.targets["end"],
        ):
            self.bubble_chamber.loggers["activity"].log(
                "Target view cannot accept suggested member."
            )
            return False
        return True

    def _fizzle(self):
        pass

    # TODO check if view's frame has been matched or not instead of checking if it has super views
    @staticmethod
    def _get_target_structure_one(parent_codelet, child_codelet):
        bubble_chamber = parent_codelet.bubble_chamber
        target_view = child_codelet.targets["view"]
        target_frame = child_codelet.targets["frame"]
        target_end = child_codelet.targets["end"]
        if target_end.is_relation:
            source_collection = bubble_chamber.interspatial_relations
            # check if target end's container frames have already been matched
            target_start_space = None
            target_end_space = None
            for sub_frame in target_frame.sub_frames:
                if (
                    target_end.start in sub_frame.input_space.contents
                    or target_end.start in sub_frame.output_space.contents
                ):
                    child_codelet.targets["start_sub_frame"] = sub_frame
                if (
                    target_end.end in sub_frame.input_space.contents
                    or target_end.end in sub_frame.output_space.contents
                ):
                    child_codelet.targets["end_sub_frame"] = sub_frame
            if (
                child_codelet.targets["start_sub_frame"]
                in target_view.matched_sub_frames
            ):
                matching_frame = target_view.matched_sub_frames[
                    child_codelet.targets["start_sub_frame"]
                ]
                child_codelet.targets["start_sub_view"] = target_view.sub_views.where(
                    parent_frame=matching_frame
                ).get()
                target_start_space = (
                    matching_frame.input_space
                    if target_end.start in target_frame.input_space.contents
                    else child_codelet.targets["start_sub_view"].output_space
                )
            if child_codelet.targets["end_sub_frame"] in target_view.matched_sub_frames:
                matching_frame = target_view.matched_sub_frames[
                    child_codelet.targets["end_sub_frame"]
                ]
                child_codelet.targets["end_sub_view"] = target_view.sub_views.where(
                    parent_frame=matching_frame
                ).get()
                target_end_space = (
                    matching_frame.input_space
                    if target_end.end in target_frame.input_space.contents
                    else child_codelet.targets["end_sub_view"].output_space
                )
            # if target end's container doesn't match, find a sub view which hasn't been matched either
            if target_start_space is None:
                potential_start_views = bubble_chamber.views.filter(
                    lambda x: x.parent_frame.parent_concept
                    == child_codelet.targets["start_sub_frame"].parent_concept
                    and x.parent_frame not in target_view.matched_sub_frames.values()
                )
                if potential_start_views.is_empty:
                    raise MissingStructureError
                potential_start_targets = StructureSet.union(
                    *[
                        view.output_space.contents.filter(lambda x: x.is_chunk)
                        if target_end.start in target_frame.output_space.contents
                        else view.parent_frame.input_space.contents.filter(
                            lambda x: x.is_chunk and (not x.is_slot or x.is_filled_in)
                        )
                        for view in potential_start_views
                    ]
                )
            else:
                potential_start_views = bubble_chamber.views.filter(
                    lambda x: target_start_space
                    in [x.parent_frame.input_space, x.output_space]
                )
                if target_end.start in target_view.grouped_nodes:
                    start_node_group = [
                        group
                        for group in target_view.node_groups
                        if target_end.start in group.values()
                    ][0]
                    try:
                        structure_one_start = start_node_group[target_start_space]
                        bubble_chamber.loggers["activity"].log(
                            f"Found structure one start: {structure_one_start}"
                        )
                    except KeyError:
                        bubble_chamber.loggers["activity"].log(
                            "Start node group has no member in target space one"
                        )
                        structure_one_start = None
                else:
                    bubble_chamber.loggers["activity"].log(
                        "Structure two start not in grouped nodes"
                    )
                    structure_one_start = None
                if structure_one_start is not None:
                    potential_start_targets = [structure_one_start]
                else:
                    potential_start_targets = StructureSet.union(
                        *[
                            view.output_space.contents.filter(lambda x: x.is_chunk)
                            if target_end.start in target_frame.output_space.contents
                            else view.parent_frame.input_space.contents.filter(
                                lambda x: x.is_chunk
                                and (not x.is_slot or x.is_filled_in)
                            )
                            for view in potential_start_views
                        ]
                    )
            if target_end_space is None:
                potential_end_views = bubble_chamber.views.filter(
                    lambda x: x.parent_frame.parent_concept
                    == child_codelet.targets["end_sub_frame"].parent_concept
                    and x.parent_frame not in target_view.matched_sub_frames.values()
                )
                if potential_end_views.is_empty:
                    raise MissingStructureError
                potential_end_targets = StructureSet.union(
                    *[
                        view.output_space.contents.filter(lambda x: x.is_chunk)
                        if target_end.start in target_frame.output_space.contents
                        else view.parent_frame.input_space.contents.filter(
                            lambda x: x.is_chunk and (not x.is_slot or x.is_filled_in)
                        )
                        for view in potential_end_views
                    ]
                )
            else:
                potential_end_views = bubble_chamber.views.filter(
                    lambda x: target_end_space
                    in [x.parent_frame.input_space, x.output_space]
                )
                if target_end.end in target_view.grouped_nodes:
                    end_node_group = [
                        group
                        for group in target_view.node_groups
                        if target_end.end in group.values()
                    ][0]
                    try:
                        structure_one_end = end_node_group[target_end_space]
                        bubble_chamber.loggers["activity"].log(
                            f"Found structure one end: {structure_one_end}"
                        )
                    except KeyError:
                        bubble_chamber.loggers["activity"].log(
                            "End node group has no member in target space one"
                        )
                        structure_one_end = None
                else:
                    bubble_chamber.loggers["activity"].log(
                        "Structure two end not in grouped nodes"
                    )
                    structure_one_end = None
                if structure_one_end is not None:
                    potential_end_targets = [structure_one_end]
                else:
                    potential_end_targets = StructureSet.union(
                        *[
                            view.output_space.contents.filter(lambda x: x.is_chunk)
                            if target_end.start in target_frame.output_space.contents
                            else view.parent_frame.input_space.contents.filter(
                                lambda x: x.is_chunk
                                and (not x.is_slot or x.is_filled_in)
                            )
                            for view in potential_end_views
                        ]
                    )
            matching_relations = source_collection.filter(
                lambda x: x.is_relation
                and x.quality > 0
                and x.start in potential_start_targets
                and x.end in potential_end_targets
                and any(
                    [
                        x.parent_concept == target_end.parent_concept,
                        target_end.parent_concept.is_slot,
                        (
                            x.parent_concept.is_compound_concept
                            and x.parent_concept.args[0] == target_end.parent_concept
                        )
                        and target_view.members.filter(
                            lambda c: c.end in target_frame.interspatial_links
                        ).not_empty,
                    ]
                )
                and target_end.parent_concept.parent_space.subsumes(
                    x.parent_concept.parent_space
                )
                and child_codelet.targets["space"].subsumes(x.conceptual_space)
                and (
                    x.parent_concept in target_end.parent_concept.possible_instances
                    if child_codelet.targets[
                        "end"
                    ].parent_concept.possible_instances.not_empty
                    else True
                )
            )
            bubble_chamber.loggers["activity"].log_set(
                matching_relations, "matching input relations"
            )
            child_codelet.targets["start"] = matching_relations.get(
                key=lambda x: x.quality * x.activation * x.uncorrespondedness
            )
            for view in bubble_chamber.views:
                if (
                    child_codelet.targets["start"].start
                    in view.parent_frame.input_space.contents
                    or child_codelet.targets["start"].start
                    in view.output_space.contents
                ):
                    child_codelet.targets["start_sub_view"] = view
                if (
                    child_codelet.targets["start"].end
                    in view.parent_frame.input_space.contents
                    or child_codelet.targets["start"].end in view.output_space.contents
                ):
                    child_codelet.targets["end_sub_view"] = view
            for sub_frame in target_frame.sub_frames:
                if (
                    target_end.start in sub_frame.input_space.contents
                    or target_end.start in sub_frame.output_space.contents
                ):
                    child_codelet.targets["start_sub_frame"] = sub_frame
                if (
                    target_end.end in sub_frame.input_space.contents
                    or target_end.end in sub_frame.output_space.contents
                ):
                    child_codelet.targets["end_sub_frame"] = sub_frame
        elif target_end.is_label:
            source_collection = bubble_chamber.interspatial_labels
            # check if target end's container frames have already been matched
            target_start_space = None
            for sub_frame in target_frame.sub_frames:
                if target_end.start in sub_frame.input_space.contents:
                    child_codelet.targets["start_sub_frame"] = sub_frame
                    if sub_frame in target_view.matched_sub_frames:
                        matching_frame = target_view.matched_sub_frames[
                            child_codelet.targets["start_sub_frame"]
                        ]
                        child_codelet.targets[
                            "start_sub_view"
                        ] = target_view.sub_views.where(
                            parent_frame=matching_frame
                        ).get()
                        target_start_space = matching_frame.input_space
                if target_end.start in sub_frame.output_space.contents:
                    child_codelet.targets["start_sub_frame"] = sub_frame
                    if sub_frame in target_view.matched_sub_frames:
                        matching_frame = target_view.matched_sub_frames[
                            child_codelet.targets["start_sub_frame"]
                        ]
                        child_codelet.targets[
                            "start_sub_view"
                        ] = target_view.sub_views.where(
                            parent_frame=matching_frame
                        ).get()
                        target_start_space = child_codelet.targets[
                            "start_sub_view"
                        ].output_space
            if target_start_space is None:
                potential_start_views = bubble_chamber.views.filter(
                    lambda x: x.parent_frame.parent_concept
                    == child_codelet.targets["start_sub_frame"].parent_concept
                    and x.parent_frame not in target_view.matched_sub_frames.values()
                    and x.unhappiness < parent_codelet.FLOATING_POINT_TOLERANCE
                    and not any(
                        [
                            x.raw_input_nodes == sub_view.raw_input_nodes
                            for sub_view in target_view.sub_views
                        ]
                    )
                )
                if potential_start_views.is_empty:
                    raise MissingStructureError
                potential_start_targets = StructureSet.union(
                    *[
                        view.output_space.contents.filter(lambda x: x.is_chunk)
                        if target_end.start in target_frame.output_space.contents
                        else view.parent_frame.input_space.contents.filter(
                            lambda x: x.is_chunk and (not x.is_slot or x.is_filled_in)
                        )
                        for view in potential_start_views
                    ]
                )
            else:
                potential_start_views = bubble_chamber.views.filter(
                    lambda x: target_start_space
                    in [x.parent_frame.input_space, x.output_space]
                )
                if target_end.start in target_view.grouped_nodes:
                    start_node_group = [
                        group
                        for group in target_view.node_groups
                        if target_end.start in group.values()
                    ][0]
                    try:
                        structure_one_start = start_node_group[target_start_space]
                        bubble_chamber.loggers["activity"].log(
                            f"Found structure one start: {structure_one_start}"
                        )
                    except KeyError:
                        bubble_chamber.loggers["activity"].log(
                            "Start node group has no member in target space one"
                        )
                        structure_one_start = None
                else:
                    bubble_chamber.loggers["activity"].log(
                        "Structure two start not in grouped nodes"
                    )
                    structure_one_start = None
                if structure_one_start is not None:
                    potential_start_targets = [structure_one_start]
                else:
                    potential_start_targets = StructureSet.union(
                        *[
                            view.output_space.contents.filter(lambda x: x.is_chunk)
                            if target_end.start in target_frame.output_space.contents
                            else view.parent_frame.input_space.contents.filter(
                                lambda x: x.is_chunk
                                and (not x.is_slot or x.is_filled_in)
                            )
                            for view in potential_start_views
                        ]
                    )
            matching_labels = source_collection.filter(
                lambda x: x.is_label
                and x.is_interspatial
                and x.correspondences.filter(
                    lambda c: c in target_view.members
                ).is_empty
                and x.quality > 0
                and x.start in potential_start_targets
                and x.parent_concept == target_end.parent_concept
                and any(
                    [
                        space1.subsumes(space2)
                        for space1 in target_end.parent_spaces.where(
                            is_conceptual_space=True
                        )
                        for space2 in x.parent_spaces.where(is_conceptual_space=True)
                    ]
                )
            )
            bubble_chamber.loggers["activity"].log_set(
                matching_labels, "matching input labels"
            )
            child_codelet.targets["start"] = matching_labels.get(
                key=lambda x: x.quality * x.activation * x.uncorrespondedness
            )
            for view in bubble_chamber.views:
                if (
                    child_codelet.targets["start"].start
                    in view.parent_frame.input_space.contents
                    or child_codelet.targets["start"].start
                    in view.output_space.contents
                ):
                    child_codelet.targets["start_sub_view"] = view
            for sub_frame in target_frame.sub_frames:
                if (
                    target_end.start in sub_frame.input_space.contents
                    or target_end.start in sub_frame.output_space.contents
                ):
                    child_codelet.targets["start_sub_frame"] = sub_frame
