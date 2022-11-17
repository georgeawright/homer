from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection_keys import (
    corresponding_exigency,
)
from linguoplotter.structure_collections import StructureDict
from linguoplotter.structures import View


class CorrespondenceSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, targets, urgency
        )

    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders import CorrespondenceBuilder

        return CorrespondenceBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
        target_view: View = None,
    ):
        from linguoplotter.codelets.suggesters.correspondence_suggesters import (
            PotentialSubFrameToFrameCorrespondenceSuggester,
            SpaceToFrameCorrespondenceSuggester,
            SubFrameToFrameCorrespondenceSuggester,
        )

        target_view = bubble_chamber.focus.view if target_view is None else target_view
        if target_view is None:
            target_view = bubble_chamber.views.filter(lambda x: x.unhappiness > 0).get()
        input_structures = target_view.parent_frame.input_space.contents.filter(
            lambda x: not x.is_correspondence
            and len(x.correspondences.where(end=x))
            < len(x.parent_spaces.where(is_contextual_space=True)) - 1
        )
        output_structures = target_view.parent_frame.output_space.contents.filter(
            lambda x: not x.is_correspondence
            and x.parent_space != target_view.parent_frame.output_space
            and x.correspondences.is_empty
        )
        if input_structures.where(is_relation=True).not_empty:
            end = input_structures.where(is_relation=True).get()
        elif input_structures.where(is_label=True).not_empty:
            end = input_structures.where(is_label=True).get()
        elif input_structures.where(is_chunk=True).not_empty:
            end = input_structures.where(is_chunk=True).get()
        elif output_structures.where(is_relation=True).not_empty:
            end = output_structures.where(is_relation=True).get()
        elif output_structures.where(is_label=True).not_empty:
            end = output_structures.where(is_label=True).get()
        elif output_structures.where(is_chunk=True).not_empty:
            end = output_structures.where(is_chunk=True).get()
        else:
            raise MissingStructureError
        possible_target_spaces = end.parent_spaces.filter(
            lambda s: s.is_contextual_space
        )
        if len(possible_target_spaces) == 1:
            target_space_two = possible_target_spaces.get()
        else:
            target_space_two = possible_target_spaces.filter(
                lambda x: x
                not in [
                    target_view.parent_frame.input_space,
                    target_view.parent_frame.output_space,
                ]
            ).get()
        if target_space_two == target_view.parent_frame.input_space:
            follow_up_class = SpaceToFrameCorrespondenceSuggester
            sub_frame = None
        else:
            sub_frame = target_view.parent_frame.sub_frames.filter(
                lambda x: target_space_two in (x.input_space, x.output_space)
            ).get()
            if sub_frame in target_view.matched_sub_frames:
                follow_up_class = SubFrameToFrameCorrespondenceSuggester
            else:
                follow_up_class = PotentialSubFrameToFrameCorrespondenceSuggester
        urgency = urgency if urgency is not None else end.uncorrespondedness
        targets = bubble_chamber.new_dict(
            {"view": target_view, "end": end, "sub_frame": sub_frame},
            name="targets",
        )
        return follow_up_class.spawn(parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = "TopDown" if targets["concept"] is not None else "BottomUp"
        codelet_id = ID.new(cls, qualifier)
        return cls(codelet_id, parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    def _passes_preliminary_checks(self):
        raise NotImplementedError

    def _calculate_confidence(self):
        if self.targets["space"] is not None:
            classification_space = (
                self.targets["end"].parent_concept.parent_space
                if self.targets["end"].is_label
                else self.targets["end"].conceptual_space
            )
        else:
            classification_space = None
        self.confidence = self.targets["concept"].classifier.classify(
            concept=self.targets["concept"],
            space=classification_space,
            start=self.targets["start"],
            end=self.targets["end"],
            view=self.targets["view"],
        )

    def _fizzle(self):
        pass

    @staticmethod
    def _get_target_conceptual_space(parent_codelet, child_codelet):
        child_codelet.targets["space"] = None
        if (
            child_codelet.targets["end"].is_link
            and child_codelet.targets["end"].is_node
        ):
            child_codelet.targets["space"] = (
                child_codelet.targets["end"]
                .parent_spaces.where(is_conceptual_space=True, is_basic_level=True)
                .get()
            )
        elif child_codelet.targets["end"].is_label:
            child_codelet.targets["space"] = child_codelet.targets[
                "end"
            ].parent_concept.parent_space
        elif child_codelet.targets["end"].is_relation:
            child_codelet.targets["space"] = child_codelet.targets[
                "end"
            ].conceptual_space

    @staticmethod
    def _get_target_structure_one(parent_codelet, child_codelet):
        source_collection = child_codelet.targets["start_space"].contents
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
                    structure_one_start = start_node_group[
                        child_codelet.targets["start_space"]
                    ]
                    parent_codelet.bubble_chamber.loggers["activity"].log(
                        f"Found structure one start: {structure_one_start}"
                    )
                except KeyError:
                    parent_codelet.bubble_chamber.loggers["activity"].log(
                        "Start node group has no member in target space one"
                    )
                    structure_one_start = None
            else:
                parent_codelet.bubble_chamber.loggers["activity"].log(
                    "Structure two start not in grouped nodes"
                )
                structure_one_start = None
        if child_codelet.targets["end"].is_label:
            if (
                child_codelet.targets["end"]
                .start.correspondences.filter(
                    lambda x: x.end == child_codelet.targets["end"].start
                    and x.start.parent_space == child_codelet.targets["start_space"]
                )
                .not_empty
            ):
                parent_codelet.bubble_chamber.loggers["activity"].log(
                    "Searching for target structure one via correspondences"
                )
                child_codelet.targets["start"] = (
                    child_codelet.targets["end"]
                    .start.correspondences.filter(
                        lambda x: x.end == child_codelet.targets["end"].start
                        and x.start.parent_space == child_codelet.targets["start_space"]
                    )
                    .get()
                    .start.labels.filter(
                        lambda x: child_codelet.targets["space"].unifies_with(
                            x.parent_concept.parent_space
                        )
                    )
                    .get()
                )
            else:
                parent_codelet.bubble_chamber.loggers["activity"].log(
                    "Searching for target structure one via source collection"
                )
                child_codelet.targets["start"] = source_collection.filter(
                    lambda x: x.is_label
                    and (
                        (x.start == structure_one_start)
                        or (structure_one_start is None)
                    )
                    and child_codelet.targets["space"].unifies_with(
                        x.parent_concept.parent_space
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
                ).get(key=corresponding_exigency)
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
                    structure_one_end = end_node_group[
                        child_codelet.targets["start_space"]
                    ]
                    parent_codelet.bubble_chamber.loggers["activity"].log(
                        f"Found structure one end: {structure_one_end}"
                    )
                except KeyError:
                    parent_codelet.bubble_chamber.loggers["activity"].log(
                        "End node group has no member in target space one"
                    )
                    structure_one_end = None
            else:
                parent_codelet.bubble_chamber.loggers["activity"].log(
                    "Structure two end not in grouped nodes"
                )
                structure_one_end = None
            matching_relations = source_collection.filter(
                lambda x: x.is_relation
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
                            and (
                                x.parent_concept.root.name != "not"
                                or child_codelet.targets["view"].members.not_empty
                            )
                        ),
                    ]
                )
                and child_codelet.targets["end"].parent_concept.parent_space.subsumes(
                    x.parent_concept.parent_space
                )
                and child_codelet.targets["space"].subsumes(x.conceptual_space)
            )
            parent_codelet.bubble_chamber.loggers["activity"].log_set(
                matching_relations, "matching input relations"
            )
            child_codelet.targets["start"] = matching_relations.get(
                key=corresponding_exigency
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
                parent_codelet.bubble_chamber.loggers["activity"].log_dict(
                    node_group, "Target structure two node group"
                )
                if child_codelet.targets["start_space"] in node_group:
                    child_codelet.targets["start"] = node_group[
                        child_codelet.targets["start_space"]
                    ]
                else:
                    for input_space in child_codelet.targets["view"].input_spaces:
                        if input_space in node_group:
                            target_structure_zero = node_group[input_space]
                            child_codelet.targets["start"] = (
                                target_structure_zero.correspondences_to_space(
                                    child_codelet.targets["start_space"]
                                )
                                .get()
                                .end
                            )
                            break
                    if child_codelet.targets["start"] is None:
                        raise MissingStructureError
            else:
                # TODO: possible defunct branch?
                parent_codelet.bubble_chamber.loggers["activity"].log(
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
