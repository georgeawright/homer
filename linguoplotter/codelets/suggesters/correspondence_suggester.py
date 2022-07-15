from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structure_collection_keys import (
    corresponding_exigency,
)
from linguoplotter.structures import View

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
            raise MissingStructureError
        input_structures = target_view.parent_frame.input_space.contents.filter(
            lambda x: not x.is_correspondence
            and len(x.correspondences.where(end=x))
            < len(x.parent_spaces.where(is_contextual_space=True)) - 1
        )
        output_structures = target_view.parent_frame.output_space.contents.filter(
            lambda x: not x.is_correspondence
            and x.parent_space != target_view.parent_frame.output_space
            and x.correspondences.is_empty()
        )
        if not input_structures.where(is_relation=True).is_empty():
            target_structure_two = input_structures.where(is_relation=True).get()
        elif not input_structures.where(is_label=True).is_empty():
            target_structure_two = input_structures.where(is_label=True).get()
        elif not input_structures.where(is_chunk=True).is_empty():
            target_structure_two = input_structures.where(is_chunk=True).get()
        elif not output_structures.where(is_relation=True).is_empty():
            target_structure_two = output_structures.where(is_relation=True).get()
        elif not output_structures.where(is_label=True).is_empty():
            target_structure_two = output_structures.where(is_label=True).get()
        elif not output_structures.where(is_chunk=True).is_empty():
            target_structure_two = output_structures.where(is_chunk=True).get()
        else:
            raise MissingStructureError
        possible_target_spaces = target_structure_two.parent_spaces.filter(
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
        urgency = (
            urgency if urgency is not None else target_structure_two.uncorrespondedness
        )
        return follow_up_class.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_space_two": target_space_two,
                "target_structure_two": target_structure_two,
                "sub_frame": sub_frame,
            },
            urgency,
        )

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

    @staticmethod
    def _get_target_conceptual_space(calling_codelet, correspondence_suggester):
        correspondence_suggester.target_conceptual_space = None
        if (
            correspondence_suggester.target_structure_two.is_link
            and correspondence_suggester.target_structure_two.is_node
        ):
            correspondence_suggester.target_conceptual_space = (
                correspondence_suggester.target_structure_two.parent_spaces.where(
                    is_conceptual_space=True, is_basic_level=True
                ).get()
            )
        elif correspondence_suggester.target_structure_two.is_label:
            correspondence_suggester.target_conceptual_space = (
                correspondence_suggester.target_structure_two.parent_concept.parent_space
            )
        elif correspondence_suggester.target_structure_two.is_relation:
            correspondence_suggester.target_conceptual_space = (
                correspondence_suggester.target_structure_two.conceptual_space
            )
        calling_codelet.bubble_chamber.loggers["activity"].log(
            calling_codelet,
            f"Found target conceptual space: {correspondence_suggester.target_conceptual_space}",
        )

    @staticmethod
    def _get_target_structure_one(calling_codelet, correspondence_suggester):
        source_collection = correspondence_suggester.target_space_one.contents
        if (
            correspondence_suggester.target_structure_two.is_label
            and correspondence_suggester.target_structure_two.start.is_label
        ):
            return CorrespondenceSuggester._get_target_structure_one_labeled_label(
                calling_codelet, correspondence_suggester, source_collection
            )
        if (
            correspondence_suggester.target_structure_two.is_link
            and correspondence_suggester.target_structure_two.is_node
        ):
            correspondence_suggester.target_structure_one = source_collection.filter(
                lambda x: x.has_location_in_space(
                    correspondence_suggester.target_conceptual_space
                )
            ).get(key=corresponding_exigency)
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
                try:
                    structure_one_start = start_node_group[
                        correspondence_suggester.target_space_one
                    ]
                    calling_codelet.bubble_chamber.loggers["activity"].log(
                        calling_codelet,
                        f"Found structure one start: {structure_one_start}",
                    )
                except KeyError:
                    calling_codelet.bubble_chamber.loggers["activity"].log(
                        calling_codelet,
                        f"Start node group has no member in target space one",
                    )
                    structure_one_start = None
            else:
                calling_codelet.bubble_chamber.loggers["activity"].log(
                    calling_codelet, f"Structure two start not in grouped nodes"
                )
                structure_one_start = None
        if correspondence_suggester.target_structure_two.is_label:
            if not correspondence_suggester.target_structure_two.start.correspondences.where(
                parent_view=correspondence_suggester.target_view,
                end=correspondence_suggester.target_structure_two.start,
            ).is_empty():
                calling_codelet.bubble_chamber.loggers["activity"].log(
                    calling_codelet,
                    "Searching for target structure one via correspondences",
                )
                correspondence_suggester.target_structure_one = (
                    correspondence_suggester.target_structure_two.start.correspondences.where(
                        parent_view=correspondence_suggester.target_view,
                        end=correspondence_suggester.target_structure_two.start,
                    )
                    .get()
                    .start.labels.filter(
                        lambda x: x.parent_concept
                        in correspondence_suggester.target_conceptual_space.contents
                    )
                    .get()
                )
            else:
                calling_codelet.bubble_chamber.loggers["activity"].log(
                    calling_codelet,
                    "Searching for target structure one via source collection",
                )
                correspondence_suggester.target_structure_one = source_collection.filter(
                    lambda x: x.is_label
                    and (
                        (x.start == structure_one_start)
                        or (structure_one_start is None)
                    )
                    and x.has_location_in_space(
                        correspondence_suggester.target_conceptual_space
                    )
                    and any(
                        [
                            x.parent_concept
                            == correspondence_suggester.target_structure_two.parent_concept,
                            x.parent_concept.is_slot,
                            correspondence_suggester.target_structure_two.parent_concept.is_slot,
                        ]
                    )
                ).get(
                    key=corresponding_exigency
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
                try:
                    structure_one_end = end_node_group[
                        correspondence_suggester.target_space_one
                    ]
                    calling_codelet.bubble_chamber.loggers["activity"].log(
                        calling_codelet, f"Found structure one end: {structure_one_end}"
                    )
                except KeyError:
                    calling_codelet.bubble_chamber.loggers["activity"].log(
                        calling_codelet,
                        f"End node group has no member in target space one",
                    )
                    structure_one_end = None
            else:
                calling_codelet.bubble_chamber.loggers["activity"].log(
                    calling_codelet, f"Structure two end not in grouped nodes"
                )
                structure_one_end = None
            calling_codelet.bubble_chamber.loggers["activity"].log_collection(
                calling_codelet,
                source_collection.filter(lambda x: x.is_relation),
                "input relations",
            )
            calling_codelet.bubble_chamber.loggers["activity"].log(
                calling_codelet, correspondence_suggester.target_conceptual_space
            )
            matching_relations = source_collection.filter(
                lambda x: x.is_relation
                and (x.start == structure_one_start or structure_one_start is None)
                and (x.end == structure_one_end or structure_one_end is None)
                and (
                    x.parent_concept
                    == correspondence_suggester.target_structure_two.parent_concept
                    or correspondence_suggester.target_structure_two.parent_concept.is_slot
                )
                and x.conceptual_space
                == correspondence_suggester.target_conceptual_space
            )
            calling_codelet.bubble_chamber.loggers["activity"].log_collection(
                calling_codelet,
                matching_relations,
                "matching input relations",
            )
            correspondence_suggester.target_structure_one = matching_relations.get(
                key=corresponding_exigency
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
                calling_codelet.bubble_chamber.loggers["activity"].log_dict(
                    calling_codelet,
                    node_group,
                    "Target structure two node group",
                )
                if correspondence_suggester.target_space_one in node_group:
                    correspondence_suggester.target_structure_one = node_group[
                        correspondence_suggester.target_space_one
                    ]
                else:
                    for (
                        input_space
                    ) in correspondence_suggester.target_view.input_spaces:
                        if input_space in node_group:
                            target_structure_zero = node_group[input_space]
                            correspondence_suggester.target_structure_one = (
                                target_structure_zero.correspondences_to_space(
                                    correspondence_suggester.target_space_one
                                )
                                .get()
                                .end
                            )
                            break
                    if correspondence_suggester.target_structure_one is None:
                        raise MissingStructureError
            else:
                calling_codelet.bubble_chamber.loggers["activity"].log(
                    calling_codelet, "Target structure two not in node group"
                )
                correspondence_suggester.target_structure_one = (
                    source_collection.filter(
                        lambda x: type(x)
                        == type(correspondence_suggester.target_structure_two)
                        and (not x.is_slot or not x.correspondences.is_empty())
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

    @staticmethod
    def _get_target_structure_one_labeled_label(
        calling_codelet, correspondence_suggester, source_collection
    ):
        bubble_chamber = calling_codelet.bubble_chamber
        labelled_slot_label = correspondence_suggester.target_structure_two.start
        bubble_chamber.loggers["activity"].log(
            calling_codelet, f"Labelled slot label: {labelled_slot_label}"
        )
        labelled_instance_label = (
            labelled_slot_label.correspondences.filter(
                lambda x: x.parent_view == correspondence_suggester.target_view
                and x.start.parent_space.is_main_input
            )
            .get()
            .start
        )
        bubble_chamber.loggers["activity"].log(
            calling_codelet, f"Labelled instance label: {labelled_instance_label}"
        )
        correspondence_suggester.target_structure_one = (
            labelled_instance_label.labels.filter(
                lambda x: x.parent_concept.has_location_in_space(
                    correspondence_suggester.target_conceptual_space
                )
            ).get()
        )
        bubble_chamber.loggers["activity"].log(
            calling_codelet,
            f"Found target structure one: {correspondence_suggester.target_structure_one}",
        )
