from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection_keys import corresponding_exigency

# TODO: possibly need restriction on space to frame correspondence suggester to prevent corresponding to sub-space items


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
        self.target_sub_view = target_structures.get("target_sub_view")
        self.sub_frame = target_structures.get("sub_frame")
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
        parent_concept = target_structures.get("parent_concept")
        qualifier = "TopDown" if parent_concept is not None else "BottomUp"
        codelet_id = ID.new(cls, qualifier)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    @property
    def targets_dict(self):
        return {
            "target_structure_one": self.target_structure_one,
            "target_structure_two": self.target_structure_two,
            "target_space_one": self.target_space_one,
            "target_space_two": self.target_space_two,
            "target_conceptual_space": self.target_conceptual_space,
            "parent_concept": self.parent_concept,
            "target_view": self.target_view,
            "target_sub_view": self.target_sub_view,
            "sub_frame": self.sub_frame,
        }

    def _passes_preliminary_checks(self):
        raise NotImplementedError

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

    def _get_target_conceptual_space(self):
        self.target_conceptual_space = None
        if self.target_structure_two.is_link and self.target_structure_two.is_node:
            self.target_conceptual_space = (
                self.target_structure_two.parent_spaces.where(
                    is_conceptual_space=True, is_basic_level=True
                ).get()
            )
        elif self.target_structure_two.is_link:
            self.target_conceptual_space = (
                self.target_structure_two.parent_concept.parent_space
            )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Found target conceptual space: {self.target_conceptual_space}"
        )

    def _get_target_structure_one(self):
        if self.target_structure_two.is_link and self.target_structure_two.is_node:
            self.target_structure_one = self.target_space_one.contents.filter(
                lambda x: x.has_location_in_space(self.target_conceptual_space)
            ).get(key=corresponding_exigency)
        if self.target_structure_two.is_link and not self.target_structure_two.is_node:
            if self.target_structure_two.start in self.target_view.grouped_nodes:
                start_node_group = [
                    group
                    for group in self.target_view.node_groups
                    if self.target_structure_two in group
                ][0]
                structure_one_start = [
                    node
                    for node in start_node_group
                    if node.parent_space == self.target_space_one
                ][0]
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found structure one start: {structure_one_start}"
                )
            else:
                structure_one_start = None
        if self.target_structure_two.is_label:
            self.target_structure_one = self.target_space_one.contents.filter(
                lambda x: x.is_label
                and (
                    x.start == structure_one_start
                    if structure_one_start is not None
                    else True
                )
                and x.has_location_in_space(self.target_conceptual_space)
            ).get(key=corresponding_exigency)
        if self.target_structure_two.is_relation:
            if self.target_structure_two.end in self.target_view.grouped_nodes:
                end_node_group = [
                    group
                    for group in self.target_view.node_groups
                    if self.target_structure_two in group
                ][0]
                structure_one_end = [
                    node
                    for node in end_node_group
                    if node.parent_space == self.target_space_one
                ][0]
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found structure one end: {structure_one_end}"
                )
            else:
                structure_one_end = None
            self.target_structure_one = self.target_space_one.contents.filter(
                lambda x: x.is_relation
                and (
                    x.start == structure_one_start
                    if structure_one_start is not None
                    else True
                )
                and (
                    x.end == structure_one_end
                    if structure_one_start is not None
                    else True
                )
                and x.conceptual_space == self.target_conceptual_space
            ).get(key=corresponding_exigency)
        if self.target_structure_two.is_node and not self.target_structure_two.is_link:
            if self.target_structure_two in self.target_view.grouped_nodes:
                node_group = [
                    group
                    for group in self.target_view.node_groups
                    if self.target_structure_two in group
                ][0]
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Target structure two in node group: {node_group}"
                )
                self.target_structure_one = [
                    node
                    for node in node_group
                    if node.parent_space == self.target_space_one
                ][0]
            else:
                self.bubble_chamber.loggers["activity"].log(
                    self, "Target structure two not in node group"
                )
                self.target_structure_one = self.target_space_one.contents.filter(
                    lambda x: type(x) == type(self.target_structure_two)
                    and (
                        x.has_location_in_space(self.target_conceptual_space)
                        if self.target_conceptual_space is not None
                        else True
                    )
                ).get(key=corresponding_exigency)
        self.bubble_chamber.loggers["activity"].log(
            self, f"Found target structure one: {self.target_structure_one}"
        )
        if self.target_structure_two.is_link and self.target_structure_two.is_node:
            self.target_structure_one = self.target_space_one.contents.filter(
                lambda x: x.has_location_in_space(self.target_conceptual_space)
            ).get(key=corresponding_exigency)
        if self.target_structure_two.is_link and not self.target_structure_two.is_node:
            if self.target_structure_two.start in self.target_view.grouped_nodes:
                start_node_group = [
                    group
                    for group in self.target_view.node_groups
                    if self.target_structure_two in group
                ][0]
                structure_one_start = [
                    node
                    for node in start_node_group
                    if node.parent_space == self.target_space_one
                ][0]
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found structure one start: {structure_one_start}"
                )
            else:
                structure_one_start = None
        if self.target_structure_two.is_label:
            self.target_structure_one = self.target_space_one.contents.filter(
                lambda x: x.is_label
                and (
                    x.start == structure_one_start
                    if structure_one_start is not None
                    else True
                )
                and x.has_location_in_space(self.target_conceptual_space)
            ).get(key=corresponding_exigency)
        if self.target_structure_two.is_relation:
            if self.target_structure_two.end in self.target_view.grouped_nodes:
                end_node_group = [
                    group
                    for group in self.target_view.node_groups
                    if self.target_structure_two in group
                ][0]
                structure_one_end = [
                    node
                    for node in end_node_group
                    if node.parent_space == self.target_space_one
                ][0]
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found structure one end: {structure_one_end}"
                )
            else:
                structure_one_end = None
            self.target_structure_one = self.target_space_one.contents.filter(
                lambda x: x.is_relation
                and (
                    x.start == structure_one_start
                    if structure_one_start is not None
                    else True
                )
                and (
                    x.end == structure_one_end
                    if structure_one_start is not None
                    else True
                )
                and x.conceptual_space == self.target_conceptual_space
            ).get(key=corresponding_exigency)
        if self.target_structure_two.is_node and not self.target_structure_two.is_link:
            if self.target_structure_two in self.target_view.grouped_nodes:
                node_group = [
                    group
                    for group in self.target_view.node_groups
                    if self.target_structure_two in group
                ][0]
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Target structure two in node group: {node_group}"
                )
                self.target_structure_one = [
                    node
                    for node in node_group
                    if node.parent_space == self.target_space_one
                ][0]
            else:
                self.bubble_chamber.loggers["activity"].log(
                    self, "Target structure two not in node group"
                )
                self.target_structure_one = self.target_space_one.contents.filter(
                    lambda x: type(x) == type(self.target_structure_two)
                    and (
                        x.has_location_in_space(self.target_conceptual_space)
                        if self.target_conceptual_space is not None
                        else True
                    )
                ).get(key=corresponding_exigency)
        self.bubble_chamber.loggers["activity"].log(
            self, f"Found target structure one: {self.target_structure_one}"
        )
