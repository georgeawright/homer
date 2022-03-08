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

    @staticmethod
    def _get_target_structure_one(calling_codelet, correspondence_suggester):
        if (
            correspondence_suggester.target_structure_two.is_link
            and correspondence_suggester.target_structure_two.is_node
        ):
            correspondence_suggester.target_structure_one = (
                correspondence_suggester.target_space_one.contents.filter(
                    lambda x: x.has_location_in_space(
                        correspondence_suggester.target_conceptual_space
                    )
                ).get(key=corresponding_exigency)
            )
        if (
            correspondence_suggester.target_structure_two.is_link
            and not correspondence_suggester.target_structure_two.is_node
        ):
            if (
                correspondence_suggester.target_structure_two.start
                in correspondence_suggester.target_view.grouped_nodes
            ):
                start_node_group = [
                    group
                    for group in correspondence_suggester.target_view.node_groups
                    if correspondence_suggester.target_structure_two.start
                    in group.values()
                ][0]
                structure_one_start = start_node_group[
                    correspondence_suggester.target_space_one
                ]
                calling_codelet.bubble_chamber.loggers["activity"].log(
                    calling_codelet, f"Found structure one start: {structure_one_start}"
                )
            else:
                structure_one_start = None
        if correspondence_suggester.target_structure_two.is_label:
            correspondence_suggester.target_structure_one = (
                correspondence_suggester.target_space_one.contents.filter(
                    lambda x: x.is_label
                    and (
                        (x.start == structure_one_start)
                        or (structure_one_start is None)
                    )
                    and x.has_location_in_space(
                        correspondence_suggester.target_conceptual_space
                    )
                ).get(key=corresponding_exigency)
            )
        if correspondence_suggester.target_structure_two.is_relation:
            if (
                correspondence_suggester.target_structure_two.end
                in correspondence_suggester.target_view.grouped_nodes
            ):
                end_node_group = [
                    group
                    for group in correspondence_suggester.target_view.node_groups
                    if correspondence_suggester.target_structure_two.end
                    in group.values()
                ][0]
                structure_one_end = end_node_group[
                    correspondence_suggester.target_space_one
                ]
                calling_codelet.bubble_chamber.loggers["activity"].log(
                    calling_codelet, f"Found structure one end: {structure_one_end}"
                )
            else:
                structure_one_end = None
            correspondence_suggester.target_structure_one = (
                correspondence_suggester.target_space_one.contents.filter(
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
                    and x.conceptual_space
                    == correspondence_suggester.target_conceptual_space
                ).get(key=corresponding_exigency)
            )
        if (
            correspondence_suggester.target_structure_two.is_node
            and not correspondence_suggester.target_structure_two.is_link
        ):
            if (
                correspondence_suggester.target_structure_two
                in correspondence_suggester.target_view.grouped_nodes
            ):
                node_group = [
                    group
                    for group in correspondence_suggester.target_view.node_groups
                    if correspondence_suggester.target_structure_two in group.values()
                ][0]
                calling_codelet.bubble_chamber.loggers["activity"].log(
                    calling_codelet,
                    f"Target structure two in node group: {node_group}",
                )
                correspondence_suggester.target_structure_one = node_group[
                    correspondence_suggester.target_space_one
                ]
            else:
                calling_codelet.bubble_chamber.loggers["activity"].log(
                    calling_codelet, "Target structure two not in node group"
                )
                correspondence_suggester.target_structure_one = (
                    correspondence_suggester.target_space_one.contents.filter(
                        lambda x: type(x)
                        == type(correspondence_suggester.target_structure_two)
                        and (
                            x.has_location_in_space(
                                correspondence_suggester.target_conceptual_space
                            )
                            if correspondence_suggester.target_conceptual_space
                            is not None
                            else True
                        )
                    ).get(key=corresponding_exigency)
                )
        calling_codelet.bubble_chamber.loggers["activity"].log(
            calling_codelet,
            f"Found target structure one: {correspondence_suggester.target_structure_one}",
        )
