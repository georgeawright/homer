from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection_keys import (
    activation,
    corresponding_exigency,
    exigency,
    quality_and_activation,
    uncorrespondedness,
)
from linguoplotter.structures.nodes import Concept


class SpaceToFrameCorrespondenceSuggester(CorrespondenceSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.correspondence_builders import (
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
        target_view = bubble_chamber.views.get(key=exigency)
        target_space_two = target_view.parent_frame.input_space
        end = target_space_two.contents.where(is_correspondence=False).get(
            key=uncorrespondedness
        )
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
        target_end_space = target_view.parent_frame.input_space
        end = target_end_space.contents.where(is_correspondence=False).get(
            key=uncorrespondedness
        )
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
                classification_space = (
                    self.targets["start"].parent_concept.parent_space
                    if self.targets["end"].is_label
                    else self.targets["start"].conceptual_space
                )
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
        if (
            self.targets["end"].is_label
            and not self.targets["space"].is_slot
            and not self.targets["start"].has_location_in_space(self.targets["space"])
        ):
            self.bubble_chamber.loggers["activity"].log(
                "Suggested concept does not have location in conceptual space"
            )
            return False
        return True

    def _calculate_confidence(self):
        input_links, input_chunks = (
            (
                self.bubble_chamber.new_set(self.targets["start"]),
                self.bubble_chamber.new_set(),
            )
            if self.targets["start"].is_link
            else (
                self.bubble_chamber.new_set(),
                self.bubble_chamber.new_set(self.targets["start"]),
            )
        )
        while input_links.not_empty:
            link = input_links.get()
            for arg in link.arguments:
                if arg.is_chunk:
                    input_chunks.add(arg)
                elif arg.is_link:
                    input_links.add(arg)
            input_links.remove(link)
        input_quality = (
            min([chunk.quality for chunk in input_chunks])
            * self.targets["start"].quality
        )
        if self.targets["space"] is not None:
            classification_space = (
                self.targets["start"].parent_concept.parent_space
                if self.targets["end"].is_label
                else self.targets["start"].conceptual_space
            )
        else:
            classification_space = None
        self.confidence = (
            self.targets["concept"].classifier.classify(
                concept=self.targets["concept"],
                space=classification_space,
                start=self.targets["start"],
                end=self.targets["end"],
                view=self.targets["view"],
            )
            * input_quality
        )

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

    @staticmethod
    def _get_target_structure_one(parent_codelet, child_codelet):
        bubble_chamber = parent_codelet.bubble_chamber
        start_space = child_codelet.targets["view"].input_spaces.get()
        source_collection = start_space.contents
        random_number = bubble_chamber.random_machine.generate_number()
        if child_codelet.targets["end"].is_link:
            if (
                child_codelet.targets["end"].start
                in child_codelet.targets["view"].grouped_nodes
            ):
                start_node_group = [
                    group
                    for group in child_codelet.targets["view"].node_groups
                    if child_codelet.targets["end"].start in group.values()
                ][0]
                try:
                    structure_one_start = start_node_group[start_space]
                except KeyError:
                    bubble_chamber.loggers["activity"].log(
                        "Start node group has no member in target space one",
                    )
                    structure_one_start = None
            else:
                bubble_chamber.loggers["activity"].log(
                    "Structure two start not in grouped nodes"
                )
                structure_one_start = None
        if child_codelet.targets["end"].is_label:
            if (
                child_codelet.targets["end"]
                .start.correspondences.where(
                    parent_view=child_codelet.targets["view"],
                    end=child_codelet.targets["end"].start,
                )
                .not_empty
            ):
                bubble_chamber.loggers["activity"].log(
                    "Searching for target structure one via correspondences"
                )
                child_codelet.targets["start"] = (
                    child_codelet.targets["end"]
                    .start.correspondences.where(
                        parent_view=child_codelet.targets["view"],
                        end=child_codelet.targets["end"].start,
                    )
                    .get()
                    .start.labels.filter(
                        lambda x: child_codelet.targets["space"].subsumes(
                            x.parent_concept.parent_spaces
                        )
                        and x.quality * x.activation > 0
                        and x.uncorrespondedness > random_number
                        and x.parent_concept
                        in child_codelet.targets[
                            "end"
                        ].parent_concept.possible_instances
                        if not child_codelet.targets[
                            "end"
                        ].parent_concept.possible_instances.is_empty
                        else True
                    )
                    .get(key=quality_and_activation)
                )
            else:
                bubble_chamber.loggers["activity"].log(
                    "Searching for target structure one via source collection"
                )
                child_codelet.targets["start"] = source_collection.filter(
                    lambda x: x.is_label
                    and (
                        (x.start == structure_one_start)
                        or (structure_one_start is None)
                    )
                    and x.start.quality * x.start.activation > 0
                    and x.quality * x.activation > 0
                    and x.uncorrespondedness > random_number
                    and child_codelet.targets["space"].subsumes(
                        x.parent_concept.parent_spaces
                    )
                    and any(
                        [
                            x.parent_concept
                            == child_codelet.targets["end"].parent_concept,
                            x.parent_concept.is_slot,
                            child_codelet.targets["end"].parent_concept.is_slot,
                            (
                                x.parent_concept.is_compound_concept
                                and x.parent_concept.args[0]
                                == child_codelet.targets["end"].parent_concept
                            ),
                        ]
                    )
                    and (
                        x.parent_concept
                        in child_codelet.targets[
                            "end"
                        ].parent_concept.possible_instances
                        if child_codelet.targets[
                            "end"
                        ].parent_concept.possible_instances.not_empty
                        else True
                    )
                ).get(key=quality_and_activation)
        if child_codelet.targets["end"].is_relation:
            if (
                child_codelet.targets["end"].end
                in child_codelet.targets["view"].grouped_nodes
            ):
                end_node_group = [
                    group
                    for group in child_codelet.targets["view"].node_groups
                    if child_codelet.targets["end"].end in group.values()
                ][0]
                try:
                    structure_one_end = end_node_group[start_space]
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
            matching_relations = source_collection.filter(
                lambda x: x.is_relation
                and all(
                    [
                        x.quality * x.activation > 0,
                        x.start.quality * x.start.activation > 0,
                        x.end.quality * x.end.activation > 0,
                        x.uncorrespondedness > random_number,
                    ]
                )
                and (x.start == structure_one_start or structure_one_start is None)
                and (x.end == structure_one_end or structure_one_end is None)
                and any(
                    [
                        x.parent_concept == child_codelet.targets["end"].parent_concept,
                        child_codelet.targets["end"].parent_concept.is_slot,
                        (
                            x.parent_concept.is_compound_concept
                            and x.parent_concept.args[0]
                            == child_codelet.targets["end"].parent_concept
                        ),
                    ]
                )
                and child_codelet.targets["end"].parent_concept.parent_space.subsumes(
                    x.parent_concept.parent_space
                )
                and child_codelet.targets["space"].subsumes(x.conceptual_space)
                and (
                    x.parent_concept
                    in child_codelet.targets["end"].parent_concept.possible_instances
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
                key=quality_and_activation
            )
        if child_codelet.targets["end"].is_node:
            if (
                child_codelet.targets["end"]
                in child_codelet.targets["view"].grouped_nodes
            ):
                node_group = [
                    group
                    for group in child_codelet.targets["view"].node_groups
                    if child_codelet.targets["end"] in group.values()
                ][0]
                bubble_chamber.loggers["activity"].log_dict(
                    node_group, "Target structure two node group"
                )
                if start_space in node_group:
                    child_codelet.targets["start"] = node_group[start_space]
                else:
                    for input_space in child_codelet.targets["view"].input_spaces:
                        if input_space in node_group:
                            target_structure_zero = node_group[input_space]
                            child_codelet.targets["start"] = (
                                target_structure_zero.correspondences_to_space(
                                    start_space
                                )
                                .get()
                                .end
                            )
                            break
                    if child_codelet.targets["start"] is None:
                        raise MissingStructureError
            else:
                # TODO: possible defunct branch?
                bubble_chamber.loggers["activity"].log(
                    "Target structure two not in node group"
                )
                child_codelet.targets["start"] = source_collection.filter(
                    lambda x: type(x) == type(child_codelet.targets["end"])
                    and (not x.is_slot or x.correspondences.not_empty)
                    and (
                        x.has_location_in_space(child_codelet.targets["space"])
                        if child_codelet.targets["space"] is not None
                        and not child_codelet.targets["space"].is_slot
                        else True
                    )
                ).get(key=corresponding_exigency)
