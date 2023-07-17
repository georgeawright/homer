from __future__ import annotations
import statistics
from typing import List

from linguoplotter import fuzzy
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.location import Location
from linguoplotter.structure import Structure
from linguoplotter.structure_collections import StructureDict, StructureSet
from linguoplotter.structures import Frame
from linguoplotter.structures.nodes import Concept
from linguoplotter.structures.space import Space
from linguoplotter.structures.spaces import ContextualSpace


class View(Structure):
    """A collection of spaces and self-consistent correspondences between them."""

    CORRESPONDENCE_WEIGHT = HyperParameters.VIEW_QUALITY_CORRESPONDENCE_WEIGHT
    INPUT_WEIGHT = HyperParameters.VIEW_QUALITY_INPUT_WEIGHT

    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        parent_frame: Frame,
        locations: List[Location],
        members: StructureSet,
        frames: StructureSet,
        input_spaces: StructureSet,
        output_space: ContextualSpace,
        quality: FloatBetweenOneAndZero,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        sub_views: StructureSet,
        super_views: StructureSet,
        cohesion_views: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
        cross_view_links: StructureSet,
        cross_view_relations: StructureDict,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations=locations,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.parent_frame = parent_frame
        self.value = None
        self.frames = frames
        self.input_spaces = input_spaces
        self.output_space = output_space
        self.members = members
        self.sub_views = sub_views
        self.super_views = super_views
        self.cohesion_views = cohesion_views
        self._node_groups = []
        self._grouped_nodes = {}
        self.matched_sub_frames = {}
        self.slot_values = {}
        self.conceptual_spaces_map = {}
        self.is_view = True
        self.cross_view_links = cross_view_links
        self.cross_view_relations = cross_view_relations
        self._cohesiveness_with = {}

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "parent_frame": self.parent_frame.structure_id,
            "frames": [frame.structure_id for frame in self.frames],
            "super_views": [view.structure_id for view in self.super_views],
            "cohesion_views": [view.structure_id for view in self.cohesion_views],
            "sub_views": [view.structure_id for view in self.sub_views],
            "input_spaces": [space.structure_id for space in self.input_spaces],
            "output_space": self.output_space.structure_id,
            "members": [correspondence.structure_id for correspondence in self.members],
            "node_groups": [
                {space.structure_id: node.structure_id for space, node in group.items()}
                for group in self._node_groups
            ],
            "grouped_nodes": [node.structure_id for node in self._grouped_nodes],
            "matched_sub_frames": {
                frame_1.structure_id: frame_2.structure_id
                for frame_1, frame_2 in self.matched_sub_frames.items()
            },
            "quality": self.quality,
            "activation": self.activation,
            "unhappiness": self.unhappiness,
            "output": self.output,
        }

    @classmethod
    def get_builder_class(cls):
        from linguoplotter.codelets.builders import ViewBuilder

        return ViewBuilder

    @classmethod
    def get_evaluator_class(cls):
        from linguoplotter.codelets.evaluators import ViewEvaluator

        return ViewEvaluator

    @classmethod
    def get_selector_class(cls):
        from linguoplotter.codelets.selectors import ViewSelector

        return ViewSelector

    @property
    def raw_input_space(self) -> Space:
        return self.input_spaces.filter(
            lambda x: x.parent_concept.name == "input"
        ).get()

    @property
    def raw_input_nodes(self):
        return StructureSet.union(
            *[
                chunk.raw_members
                for chunk in StructureSet.union(
                    *[
                        c.arguments
                        for c in self.members.filter(lambda x: x.start.is_chunk)
                    ]
                    + [
                        c.start.arguments
                        for c in self.members.filter(lambda x: x.start.is_link)
                    ]
                ).filter(lambda x: x.parent_space.is_main_input)
            ]
        )

    @property
    def input_contextual_spaces(self):
        return self.input_spaces.where(is_contextual_space=True)

    @property
    def input_slots(self):
        return self.parent_frame.input_space.contents.where(is_slot=True)

    @property
    def output_sub_frame_slots(self):
        return self.parent_frame.output_space.contents.filter(
            lambda x: x.is_slot
            and len(x.parent_spaces.where(is_contextual_space=True)) > 1
        )

    @property
    def all_sub_views(self) -> StructureSet:
        return StructureSet.union(
            *[self.sub_views] + [sub_view.all_sub_views for sub_view in self.sub_views]
        )

    @property
    def grouped_links(self) -> StructureSet:
        return StructureSet.difference(
            StructureSet.union(
                *[self.members]
                + [m.arguments.where(is_link=True) for m in self.members]
            ),
            self.members,
        )

    @property
    def size(self):
        return len(self.members)

    @property
    def structures(self):
        return [
            correspondence.start
            for correspondence in self.members
            if correspondence.start.parent_space in self.input_spaces
        ] + [
            node
            for node in self.grouped_nodes
            if node.parent_space in self.input_spaces
        ]

    @property
    def slots(self):
        return self.parent_frame.slots

    @property
    def is_recyclable(self) -> bool:
        return self.activation < self.FLOATING_POINT_TOLERANCE

    @property
    def unfilled_cross_view_structures(self):
        return self.parent_frame.unfilled_cross_view_structures

    @property
    def unfilled_sub_frame_input_structures(self):
        return self.parent_frame.unfilled_sub_frame_input_structures

    @property
    def unfilled_input_structures(self):
        return self.parent_frame.unfilled_input_structures

    @property
    def unfilled_output_structures(self):
        return self.parent_frame.unfilled_output_structures

    @property
    def unfilled_projectable_structures(self):
        return self.parent_frame.unfilled_projectable_structures

    @property
    def grouped_nodes(self):
        if self.super_views.is_empty:
            return self._grouped_nodes
        return self.super_views.get().grouped_nodes

    @property
    def node_groups(self):
        if self.super_views.is_empty:
            return self._node_groups
        return self.super_views.get().node_groups

    @property
    def output(self):
        return ". ".join(
            [
                chunk.name
                for chunk in self.output_space.contents.filter(
                    lambda x: x.is_letter_chunk
                    and x.name is not None
                    and (
                        x.super_chunks.is_empty
                        or (
                            x.super_chunks.not_empty and x.most_super_chunk.name is None
                        )
                    )
                )
            ]
        )

    @property
    def number_of_items_left_to_process(self):
        return sum(
            [
                len(self.unfilled_cross_view_structures),
                len(self.unfilled_sub_frame_input_structures),
                len(self.unfilled_input_structures),
                len(self.unfilled_output_structures),
                len(self.unfilled_projectable_structures),
            ]
        )

    @property
    def has_correspondences_to_input(self):
        return self.members.filter(
            lambda x: x.start.parent_space in self.input_spaces
        ).not_empty

    def recalculate_unhappiness(self):
        self.unhappiness = 1 - 0.5**self.parent_frame.number_of_items_left_to_process

    def recalculate_salience(self):
        self.recalculate_unhappiness()
        self.salience = fuzzy.AND(self.unhappiness, self.activation)

    def calculate_quality(self):
        for member in self.members:
            if (
                member.parent_concept.is_compound_concept
                and member.parent_concept.root.name == "not"
            ):
                return 0.0
        relevant_correspondences = self.members.filter(
            lambda x: x.parent_view == self
            and not (
                not x.start.is_slot
                and x.start in self.parent_frame.output_space.contents
            )
        )
        total_slots = (
            len(relevant_correspondences) + self.number_of_items_left_to_process
        )
        correspondence_quality = (
            sum(correspondence.quality for correspondence in relevant_correspondences)
            / total_slots
        )
        try:
            input_quality = statistics.fmean(
                [
                    correspondence.start.quality
                    * correspondence.end.parent_concept.number_of_components
                    if correspondence.end.is_link
                    else correspondence.start.quality
                    for correspondence in self.members
                    if correspondence.start.parent_space is not None
                    and correspondence.start.parent_space.is_main_input
                ]
            )
        except ValueError:
            input_quality = 0
        return fuzzy.AND(correspondence_quality, input_quality)

    def is_equivalent_to(self, other: View):
        try:
            return self.structures == other.structures and self.output == other.output
        except MissingStructureError:
            return False

    def is_competing_with(self, other: View):
        return (
            self != other
            and self.parent_frame.parent_concept == other.parent_frame.parent_concept
            and self.has_correspondences_to_input
            and other.has_correspondences_to_input
            and self.raw_input_nodes == other.raw_input_nodes
            and other.super_views.is_empty
            or self.is_competing_cohesion_view_with(other)
        )

    def is_competing_cohesion_view_with(self, other: View):
        return any([other in sub_view.cohesion_views for sub_view in self.sub_views])

    def add_cross_view_relation(self, relation: "Relation"):
        self.cross_view_links.add(relation)
        other_view = (
            relation.start_view if relation.start_view != self else relation.end_view
        )
        self.cross_view_relations[other_view].add(relation)
        self.recalculate_cohesiveness_with(other_view)

    def remove_cross_view_relation(self, relation: "Relation"):
        other_view = (
            relation.start_view if relation.start_view != self else relation.end_view
        )
        self.cross_view_relations[other_view].remove(relation)
        self.recalculate_cohesiveness_with(other_view)

    def recalculate_cohesiveness_with(self, other: View):
        try:
            relations = self.cross_view_relations[other]
        except KeyError:
            self._cohesiveness_with[other] = 0.0
        try:
            words = self.output_space.contents.filter(
                lambda x: x.is_letter_chunk and x.members.is_empty
            )
            self._cohesiveness_with[other] = FloatBetweenOneAndZero(
                sum([r.quality for r in relations]) / (len(words))
            )
        except ZeroDivisionError:
            self._cohesiveness_with[other] = 0.0

    def cohesiveness_with(self, other: View) -> FloatBetweenOneAndZero:
        try:
            return self._cohesiveness_with[other]
        except KeyError:
            return 0.0

    def specify_space(self, abstract_space, conceptual_space):
        if (
            abstract_space in self.parent_frame.input_space.conceptual_spaces
            or abstract_space in self.parent_frame.output_space.conceptual_spaces
        ):
            self.conceptual_spaces_map[conceptual_space] = abstract_space
        if abstract_space in self.conceptual_spaces_map:
            self.conceptual_spaces_map.pop(abstract_space)
        for frame in self.frames:
            frame.specify_space(abstract_space, conceptual_space)
        for view in self.super_views:
            view.specify_space(abstract_space, conceptual_space)

    def add(self, correspondence: "Correspondence", verbose: bool = False):
        self.members.add(correspondence)
        # If connecting a relation with one argument, merge arguments of correspondees
        if (
            correspondence.start.is_relation
            and len(correspondence.start.arguments) == 1
            and len(correspondence.end.arguments) > 1
        ):
            old_end = correspondence.end.end
            for link in old_end.links_out:
                link.start = correspondence.end.start
                link.arguments.remove(old_end)
                link.arguments.add(correspondence.end.start)
                correspondence.end.start.links_out.add(link)
                if link.is_relation and link.parent_concept.is_slot:
                    link._parent_concept = (
                        link.parent_concept.possible_instances.where(name="same")
                    ).get()
            for link in old_end.links_in:
                link.end = correspondence.end.start
                link.arguments.remove(old_end)
                correspondence.end.start.links_in.add(link)
                if link.is_relation and link.parent_concept.is_slot:
                    link._parent_concept = (
                        link.parent_concept.possible_instances.where(name="same")
                    ).get()
            old_end.parent_space.contents.remove(old_end)
        for node_pair in correspondence.node_pairs:
            for node_group in self._node_groups:
                if (
                    node_group.get(node_pair[0].parent_space) == node_pair[0]
                    or node_group.get(node_pair[1].parent_space) == node_pair[1]
                ):
                    node_group[node_pair[0].parent_space] = node_pair[0]
                    node_group[node_pair[1].parent_space] = node_pair[1]
                    self._grouped_nodes[node_pair[0]] = True
                    self._grouped_nodes[node_pair[1]] = True
                    for space in node_group:
                        if space.is_main_input:
                            for _, node in node_group.items():
                                node._non_slot_value = node_group[space]
            if (
                node_pair[0] not in self._grouped_nodes
                or node_pair[1] not in self._grouped_nodes
            ):
                self._node_groups.append(
                    {
                        node_pair[0].parent_space: node_pair[0],
                        node_pair[1].parent_space: node_pair[1],
                    }
                )
                self._grouped_nodes[node_pair[0]] = True
                self._grouped_nodes[node_pair[1]] = True
                if node_pair[0].parent_space.is_main_input:
                    node_pair[1]._non_slot_value = node_pair[0]
        for super_view in self.super_views:
            super_view.add(correspondence)

    def remove(self, correspondence: "Correspondence"):
        self.members.remove(correspondence)
        for node_pair in correspondence.node_pairs:
            node_pair[1]._non_slot_value = None
        if (
            correspondence.parent_view == self
            and correspondence.end.is_link
            and correspondence.end.parent_concept.is_slot
        ):
            if correspondence.end.is_cross_view or not any(
                [
                    item.is_link
                    and item.parent_concept == correspondence.end.parent_concept
                    and item != correspondence.end
                    for item in correspondence.end.parent_space.contents.where(
                        is_link=True
                    )
                ]
            ):
                correspondence.end.parent_concept._non_slot_value = None
        if (
            correspondence.parent_view == self
            and correspondence.conceptual_space is not None
        ):
            if not any(
                [
                    c.conceptual_space == correspondence.conceptual_space
                    for c in self.members.excluding(correspondence)
                ]
            ):
                try:
                    self.specify_space(
                        correspondence.conceptual_space,
                        correspondence.parent_view.conceptual_spaces_map[
                            correspondence.conceptual_space
                        ],
                    )
                except KeyError:
                    pass
        for sub_frame, matched_frame in self.matched_sub_frames.copy().items():
            if (
                correspondence in matched_frame.input_space.contents
                or correspondence in matched_frame.output_space.contents
            ):
                if self.members.filter(
                    lambda x: x in matched_frame.input_space.contents
                    or x in matched_frame.output_space.contents
                ).is_empty:
                    try:
                        sub_view = self.sub_views.where(
                            parent_frame=matched_frame
                        ).get()
                        sub_view.super_views.remove(self)
                        self.sub_views.remove(sub_view)
                    except MissingStructureError:
                        pass
                    self.frames.remove(sub_frame)
                    self.matched_sub_frames.pop(sub_frame)
        self._grouped_nodes = {}
        self._node_groups = []
        for member in self.members:
            self.add(member)
        for super_view in self.super_views:
            super_view.remove(correspondence)
        self.recalculate_salience()

    def has_member(
        self,
        parent_concept: Concept,
        conceptual_space: Space,
        start: Structure,
        end: Structure,
    ) -> bool:
        return self.members.where(
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            start=start,
            end=end,
        ).not_empty

    def can_accept_member(
        self,
        parent_concept: Concept,
        conceptual_space: Space,
        start: Structure,
        end: Structure,
        sub_view: View = None,
        verbose=False,
    ) -> bool:
        if self.has_member(parent_concept, conceptual_space, start, end):
            if verbose:
                print("1")
            return False
        if (
            end.is_link
            and end.is_cross_view
            and sub_view is not None
            and end.correspondences.filter(
                lambda x: x.end == end and x not in sub_view.members
            ).not_empty
        ):
            if verbose:
                print(end.correspondences)
                print("1.1")
            return False
        if (
            end.is_relation
            and len(start.arguments) == 1
            and any(
                [
                    r.parent_concept.possible_instances.where(name="same").is_empty
                    and r.parent_concept.name != "same"
                    for r in StructureSet.intersection(
                        end.start.relations, end.end.relations
                    )
                ]
            )
        ):
            return False
        if (
            start.is_link
            and start.is_cross_view
            and start.correspondences.filter(lambda x: x in self.members).not_empty
        ):
            if verbose:
                print("1.2")
            return False
        if (
            start.is_link
            and end.is_link
            and (not start.parent_concept.is_slot or start.parent_concept.is_filled_in)
        ):
            start_concept = (
                start.parent_concept
                if not start.parent_concept.is_slot
                else start.parent_concept.non_slot_value
            )
            end_concept = end.parent_concept
            if end_concept.is_slot:
                for relative in end_concept.relatives.filter(
                    lambda x: x in self.parent_frame.concepts
                ):
                    relation_concept = (
                        end_concept.relations_with(relative).get().parent_concept
                    )
                    if relation_concept.name == "different":
                        continue
                    if relative.is_slot and relative.is_filled_in:
                        relative_concept = relative.non_slot_value
                        if not start_concept.has_relation_with(
                            relative_concept, relation_concept
                        ):
                            if verbose:
                                print("2")
                            return False
                    if not relative.is_slot:
                        if not start_concept.has_relation_with(
                            end_concept, relation_concept
                        ):
                            if verbose:
                                print("3")
                            return False
            different_concepts = end_concept.relatives.filter(
                lambda x: not x.relations_with(end_concept)
                .where(name="different")
                .is_empty
            )
            if start_concept in different_concepts:
                if verbose:
                    print("4")
                return False
        if end.correspondences.filter(
            lambda x: x.end == end
            and x in self.members
            and x.start
            and start.parent_space is not None
            and x.start in start.parent_space.contents
        ).not_empty:
            if verbose:
                print("5")
            return False
        potential_node_groups = (
            [{start.parent_space: start, end.parent_space: end}]
            if start.is_node
            else [
                {
                    start.start.parent_space: start.start,
                    end.start.parent_space: end.start,
                }
            ]
            if start.is_label
            else [
                {
                    start.start.parent_space: start.start,
                    end.start.parent_space: end.start,
                },
                {
                    start.end.parent_space: start.end,
                    end.end.parent_space: end.end,
                },
            ]
        )
        if sub_view is not None:
            for potential_node_group in potential_node_groups:
                for sub_view_node_group in sub_view.node_groups:
                    if any(
                        [
                            node in sub_view_node_group.values()
                            for node in potential_node_group.values()
                        ]
                    ):
                        for space in sub_view_node_group:
                            potential_node_group[space] = sub_view_node_group[space]
        if not all(
            [
                node.links.where(is_cross_view=True).not_empty
                for group in potential_node_groups
                for node in group.values()
            ]
        ):
            for existing_node_group in self.node_groups:
                for potential_group in potential_node_groups:
                    shared_spaces = [
                        space
                        for space in existing_node_group
                        if space in potential_group
                    ]
                    if (
                        len(shared_spaces) > 1
                        and any(
                            existing_node_group[space] == potential_group[space]
                            for space in shared_spaces
                        )
                        and not all(
                            existing_node_group[space] == potential_group[space]
                            for space in shared_spaces
                        )
                    ):
                        if verbose:
                            print("6")
                            print(existing_node_group)
                            print(potential_group)
                            print(shared_spaces)
                        return False
        if verbose:
            print("super")
        return all(
            [
                super_view.can_accept_member(
                    parent_concept,
                    conceptual_space,
                    start,
                    end,
                )
                for super_view in self.super_views
            ]
        )

    def boost_activation(self, amount: float):
        if self.is_stable:
            return
        self._activation_buffer = FloatBetweenOneAndZero(self.activation + amount)

    def recalculate_activation(self):
        self._activation_buffer = FloatBetweenOneAndZero(
            self.activation + self._activation_buffer
        )

    def __repr__(self) -> str:
        inputs = ", ".join([space.structure_id for space in self.input_spaces])
        return f"<{self.structure_id} {self.parent_frame.name}>"
