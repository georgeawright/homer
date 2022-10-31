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
        target_structure_two = target_space_two.contents.where(
            is_correspondence=False
        ).get(key=uncorrespondedness)
        urgency = (
            urgency if urgency is not None else target_structure_two.uncorrespondedness
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_space_two": target_space_two,
                "target_structure_two": target_structure_two,
            },
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.views.get(key=activation)
        target_space_two = target_view.parent_frame.input_space
        target_structure_two = target_space_two.contents.where(
            is_correspondence=False
        ).get(key=uncorrespondedness)
        urgency = (
            urgency if urgency is not None else target_structure_two.uncorrespondedness
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_space_two": target_space_two,
                "target_structure_two": target_structure_two,
                "parent_concept": parent_concept,
            },
            urgency,
        )

    def _passes_preliminary_checks(self):
        self._get_target_conceptual_space(self, self)
        if (
            self.target_structure_one is not None
            and self.parent_concept is not None
            and not (
                self.target_view.members.is_empty()
                and self.target_view.super_views.is_empty()
            )
        ):
            if (
                self.target_conceptual_space is not None
                and self.target_conceptual_space.is_slot
            ):
                classification_space = (
                    self.target_structure_one.parent_concept.parent_space
                    if self.target_structure_two.is_label
                    else self.target_structure_one.conceptual_space
                )
            else:
                classification_space = self.target_conceptual_space
            classification = self.parent_concept.classifier.classify(
                concept=self.parent_concept,
                space=classification_space,
                start=self.target_structure_one,
                end=self.target_structure_two,
                view=self.target_view,
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Preliminary classification: {classification}"
            )
            if classification < 0.5:
                self.parent_concept = self.bubble_chamber.new_compound_concept(
                    self.bubble_chamber.concepts["not"], [self.parent_concept]
                )
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found parent concept: {self.parent_concept}"
                )
        else:
            self.parent_concept = self.bubble_chamber.concepts["same"]
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found parent concept: {self.parent_concept}"
            )
        try:
            if self.target_space_one is None:
                self.target_space_one = self.target_view.input_spaces.get()
                self.bubble_chamber.loggers["activity"].log(
                    self, f"Found target space one: {self.target_space_one}"
                )
            if self.target_structure_one is None:
                self._get_target_structure_one(self, self)
        except MissingStructureError:
            self.bubble_chamber.loggers["activity"].log(
                self,
                "MissingStructureError when searching for input target space and structure",
            )
            return False
        if not self.target_view.can_accept_member(
            self.parent_concept,
            self.target_conceptual_space,
            self.target_structure_one,
            self.target_structure_two,
        ):
            self.bubble_chamber.loggers["activity"].log(
                self, "Target view cannot accept suggested member."
            )
            return False
        if (
            self.target_structure_two.is_link
            and self.target_structure_two.parent_concept.is_slot
            and not self.target_structure_two.parent_concept.is_filled_in
        ):
            structure_two_non_slot_value = self.target_structure_one.parent_concept
            for relative in self.target_structure_two.parent_concept.relatives:
                if self.target_view.parent_frame.input_space.contents.where(
                    is_link=True, parent_concept=relative
                ).is_empty():
                    relation_with_relative = (
                        self.target_structure_two.parent_concept.relations_with(
                            relative
                        ).get()
                    )
                    structure_two_parent_relatives = (
                        structure_two_non_slot_value.relatives
                    )
                    if structure_two_parent_relatives.filter(
                        lambda x: x in relative.parent_space.contents
                        and x.has_relation_with(
                            structure_two_non_slot_value,
                            relation_with_relative.parent_concept.non_slot_value,
                        )
                    ).is_empty():
                        self.bubble_chamber.loggers["activity"].log(
                            self,
                            f"None of structure two parent relatives have relation with concept",
                        )
                        return False
        return True

    def _calculate_confidence(self):
        input_links = self.bubble_chamber.new_structure_collection(
            self.target_structure_one
        )
        input_chunks = self.bubble_chamber.new_structure_collection()
        while not input_links.is_empty():
            link = input_links.get()
            for arg in link.arguments:
                if arg.is_chunk:
                    input_chunks.add(arg)
                elif arg.is_link:
                    input_links.add(arg)
            input_links.remove(link)
        input_quality = (
            min([chunk.quality for chunk in input_chunks])
            * self.target_structure_one.quality
        )
        if self.target_conceptual_space is not None:
            classification_space = (
                self.target_structure_one.parent_concept.parent_space
                if self.target_structure_two.is_label
                else self.target_structure_one.conceptual_space
            )
        else:
            classification_space = None
        self.confidence = (
            self.parent_concept.classifier.classify(
                concept=self.parent_concept,
                space=classification_space,
                start=self.target_structure_one,
                end=self.target_structure_two,
                view=self.target_view,
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
    def _get_target_structure_one(calling_codelet, correspondence_suggester):
        source_collection = correspondence_suggester.target_space_one.contents
        if correspondence_suggester.target_structure_two.is_link:
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
                        lambda x: correspondence_suggester.target_conceptual_space.subsumes(
                            x.parent_concept.parent_space
                        )
                        and x.parent_concept
                        in correspondence_suggester.target_structure_two.parent_concept.possible_instances
                        if not correspondence_suggester.target_structure_two.parent_concept.possible_instances.is_empty()
                        else True
                    )
                    .get(key=quality_and_activation)
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
                    and x.start.quality > 0
                    and x.quality > 0
                    and correspondence_suggester.target_conceptual_space.subsumes(
                        x.parent_concept.parent_space
                    )
                    and any(
                        [
                            x.parent_concept
                            == correspondence_suggester.target_structure_two.parent_concept,
                            x.parent_concept.is_slot,
                            correspondence_suggester.target_structure_two.parent_concept.is_slot,
                            (
                                x.parent_concept.is_compound_concept
                                and x.parent_concept.args[0]
                                == correspondence_suggester.target_structure_two.parent_concept
                            ),
                        ]
                    )
                    and (
                        x.parent_concept
                        in correspondence_suggester.target_structure_two.parent_concept.possible_instances
                        if not correspondence_suggester.target_structure_two.parent_concept.possible_instances.is_empty()
                        else True
                    )
                ).get(
                    key=quality_and_activation
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
            matching_relations = source_collection.filter(
                lambda x: x.is_relation
                and all([x.quality > 0, x.start.quality > 0, x.end.quality > 0])
                and (x.start == structure_one_start or structure_one_start is None)
                and (x.end == structure_one_end or structure_one_end is None)
                and any(
                    [
                        x.parent_concept
                        == correspondence_suggester.target_structure_two.parent_concept,
                        correspondence_suggester.target_structure_two.parent_concept.is_slot,
                        (
                            x.parent_concept.is_compound_concept
                            and x.parent_concept.args[0]
                            == correspondence_suggester.target_structure_two.parent_concept
                        ),
                    ]
                )
                and correspondence_suggester.target_structure_two.parent_concept.parent_space.subsumes(
                    x.parent_concept.parent_space
                )
                and correspondence_suggester.target_conceptual_space.subsumes(
                    x.conceptual_space
                )
                and (
                    x.parent_concept
                    in correspondence_suggester.target_structure_two.parent_concept.possible_instances
                    if not correspondence_suggester.target_structure_two.parent_concept.possible_instances.is_empty()
                    else True
                )
            )
            calling_codelet.bubble_chamber.loggers["activity"].log_collection(
                calling_codelet,
                matching_relations,
                "matching input relations",
            )
            correspondence_suggester.target_structure_one = matching_relations.get(
                key=quality_and_activation
            )
        if correspondence_suggester.target_structure_two.is_node:
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
                # TODO: possible defunct branch?
                calling_codelet.bubble_chamber.loggers["activity"].log(
                    calling_codelet, "Target structure two not in node group"
                )
                correspondence_suggester.target_structure_one = source_collection.filter(
                    lambda x: type(x)
                    == type(correspondence_suggester.target_structure_two)
                    and (not x.is_slot or not x.correspondences.is_empty())
                    and (
                        x.has_location_in_space(
                            correspondence_suggester.target_conceptual_space
                        )
                        if correspondence_suggester.target_conceptual_space is not None
                        and not correspondence_suggester.target_conceptual_space.is_slot
                        else True
                    )
                ).get(
                    key=corresponding_exigency
                )
        calling_codelet.bubble_chamber.loggers["activity"].log(
            calling_codelet,
            f"Found target structure one: {correspondence_suggester.target_structure_one}",
        )
