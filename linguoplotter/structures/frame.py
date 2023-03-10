from __future__ import annotations

import math

from linguoplotter import fuzzy
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure import Structure
from linguoplotter.structure_collections import StructureSet


class Frame(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: "Concept",
        parent_frame: Frame,
        sub_frames: StructureSet,  # collection of frames (all slots)
        # structures have locations in frame and sub-frame spaces
        concepts: StructureSet,
        interspatial_links: StructureSet,
        input_space: "ContextualSpace",
        output_space: "ContextualSpace",
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        instances: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
        is_sub_frame: bool = False,
        depth: int = None,
    ):
        quality = 1
        Structure.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            locations=[],
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.name = name
        self._parent_concept = parent_concept
        self.parent_frame = parent_frame
        self.sub_frames = sub_frames
        self.concepts = concepts
        self.interspatial_links = interspatial_links
        self.input_space = input_space
        self.output_space = output_space
        self.slot_values = {}
        self.instances = instances
        self._depth = depth
        self.is_sub_frame = is_sub_frame
        self.is_frame = True
        self.parent_view = None

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "name": self.name,
            "input_space": self.input_space.structure_id,
            "output_space": self.output_space.structure_id,
            "activation": self.activation,
        }

    @property
    def depth(self) -> FloatBetweenOneAndZero:
        return self._depth if self._depth is not None else self.parent_concept.depth

    @property
    def slots(self) -> StructureSet:
        return StructureSet.union(
            self.input_space.contents.where(is_slot=True),
            self.output_space.contents.where(is_slot=True),
        )

    @property
    def items(self) -> StructureSet:
        return StructureSet.union(
            self.input_space.contents,
            self.output_space.contents,
            *[sub_frame.items for sub_frame in self.sub_frames],
        ).where(is_correspondence=False)

    @property
    def correspondences(self) -> StructureSet:
        return self.parent_view.members.filter(
            lambda x: any(
                [
                    x.start in self.input_space.contents,
                    x.start in self.output_space.contents,
                    x.end in self.input_space.contents,
                    x.end in self.output_space.contents,
                ]
            )
        )

    @property
    def conceptual_spaces(self) -> StructureSet:
        return StructureSet.union(
            self.input_space.conceptual_spaces, self.output_space.conceptual_spaces
        )

    @property
    def progenitor(self) -> Frame:
        self_progenitor = self
        while self_progenitor.parent_frame is not None:
            self_progenitor = self_progenitor.parent_frame
        return self_progenitor

    @property
    def unfilled_interspatial_structures(self):
        return self.interspatial_links.filter(
            lambda x: x.correspondences.where(end=x).is_empty
        )

    @property
    def unfilled_sub_frame_input_structures(self):
        return self.input_space.contents.filter(
            lambda x: not x.is_correspondence
            and not x.is_interspatial
            and not x.is_chunk
            and (
                len(x.correspondences.where(end=x))
                < len(x.parent_spaces.where(is_contextual_space=True)) - 1
            )
        )

    @property
    def unfilled_input_structures(self):
        return self.input_space.contents.filter(
            lambda x: not x.is_correspondence
            and not x.is_interspatial
            and not x.is_chunk
            and x.correspondences.where(end=x).is_empty
        )

    @property
    def unfilled_output_structures(self):
        return self.output_space.contents.filter(
            lambda x: not x.is_correspondence
            and not x.is_interspatial
            and x.links.where(is_interspatial=True).is_empty
            and x.parent_space != self.output_space
            and x.correspondences.where(end=x).is_empty
        )

    @property
    def unfilled_projectable_structures(self):
        return self.output_space.contents.filter(
            lambda x: not x.is_correspondence
            and not x.is_interspatial
            and x.links.where(is_interspatial=True).is_empty
            and x.correspondences.filter(lambda c: c.start == x).is_empty
        )

    @property
    def number_of_items_left_to_process(self):
        return sum(
            [
                len(self.unfilled_interspatial_structures),
                len(self.unfilled_sub_frame_input_structures),
                len(self.unfilled_input_structures),
                len(self.unfilled_output_structures),
                len(self.unfilled_projectable_structures),
            ]
        )

    @property
    def has_failed_to_match(self) -> bool:
        return any(
            [
                correspondence.parent_concept.is_compound_concept
                and correspondence.parent_concept.root.name == "not"
                for correspondence in self.correspondences
            ]
        )

    def is_equivalent_to(self, other: Frame) -> bool:
        if self.progenitor != other.progenitor:
            return False
        for space in other.conceptual_spaces:
            if not space.is_slot and space not in self.conceptual_spaces:
                return False
        for space in self.conceptual_spaces:
            if not space.is_slot and space not in other.conceptual_spaces:
                return False
        return True

    def recalculate_unhappiness(self):
        self.unhappiness = 1 / (
            sum([instance.activation for instance in self.instances]) + 1
        )

    def recalculate_exigency(self):
        self.recalculate_unhappiness()
        self.exigency = fuzzy.AND(self.unhappiness, self.activation)

    def specify_space(self, abstract_space, conceptual_space):
        if abstract_space in self.input_space.conceptual_spaces:
            self.input_space.conceptual_spaces.remove(abstract_space)
            self.input_space.conceptual_spaces.add(conceptual_space)
        if abstract_space in self.output_space.conceptual_spaces:
            self.output_space.conceptual_spaces.remove(abstract_space)
            self.output_space.conceptual_spaces.add(conceptual_space)
        if abstract_space.parent_concept in self.concepts:
            self.concepts.remove(abstract_space.parent_concept)
        self.concepts.add(conceptual_space.parent_concept)
        for item in StructureSet.union(
            self.input_space.contents,
            self.output_space.contents,
            self.interspatial_links,
        ):
            if item.parent_space == abstract_space:
                item.parent_space = conceptual_space
            if item.is_relation and item.conceptual_space == abstract_space:
                item.conceptual_space = conceptual_space
            for location in item.locations:
                if location.space != abstract_space:
                    continue
                try:
                    item.location_in_space(abstract_space).coordinates = [
                        [math.nan for _ in range(conceptual_space.no_of_dimensions)]
                    ]
                    item.location_in_space(abstract_space).space = conceptual_space
                    conceptual_space.add(item)
                    item.parent_spaces.remove(abstract_space)
                    item.parent_spaces.add(conceptual_space)
                except NotImplementedError:
                    item.location_in_space(abstract_space).start_coordinates = [
                        [math.nan for _ in range(conceptual_space.no_of_dimensions)]
                    ]
                    item.location_in_space(abstract_space).end_coordinates = [
                        [math.nan for _ in range(conceptual_space.no_of_dimensions)]
                    ]
                    item.location_in_space(abstract_space).space = conceptual_space
                    conceptual_space.add(item)
                    item.parent_spaces.remove(abstract_space)
                    item.parent_spaces.add(conceptual_space)
        for concept in self.concepts:
            if concept.parent_space == abstract_space:
                concept.parent_space = conceptual_space
            if abstract_space in concept.parent_spaces:
                concept.parent_spaces.remove(abstract_space)
                concept.parent_spaces.add(conceptual_space)
                concept.location_in_space(abstract_space).space = conceptual_space

    def instantiate(
        self,
        input_space: "ContextualSpace",
        conceptual_spaces_map: dict,
        parent_id: str,
        bubble_chamber,
        input_copies: dict = None,
        output_copies: dict = None,
    ):
        input_copies = {} if input_copies is None else input_copies
        output_copies = {} if output_copies is None else output_copies
        # need to copy the concepts to prevent interference between frame instances
        # concepts may need spaces to be changed due to space specification
        concept_copies = {}
        for concept in self.concepts:
            concept_copies[concept] = concept.copy(
                bubble_chamber=bubble_chamber, parent_id=parent_id
            )
            for relation in concept.relations:
                if (
                    relation.start in concept_copies
                    and relation.end in concept_copies
                    and (
                        relation.parent_concept in concept_copies
                        or not relation.parent_concept.is_slot
                    )
                ):
                    new_relation = relation.copy(
                        bubble_chamber=bubble_chamber,
                        parent_id=parent_id,
                        start=concept_copies[relation.start],
                        end=concept_copies[relation.end],
                    )
                    if relation.parent_concept.is_slot:
                        new_relation._parent_concept = concept_copies[
                            relation.parent_concept
                        ]
                    concept_copies[relation.start].links_out.add(new_relation)
                    concept_copies[relation.end].links_in.add(new_relation)
        concepts = bubble_chamber.new_set(*[new for old, new in concept_copies.items()])
        output_space = (
            self.output_space if input_space == self.input_space else self.input_space
        )
        input_space_copy, input_copies = input_space.copy(
            bubble_chamber=bubble_chamber, parent_id=parent_id, copies=input_copies
        )
        for structure in input_space_copy.contents.where(is_link=True):
            if structure.parent_concept in concept_copies:
                structure._parent_concept = concept_copies[structure.parent_concept]
        output_space_copy, output_copies = output_space.copy(
            bubble_chamber=bubble_chamber, parent_id=parent_id, copies=output_copies
        )
        for structure in output_space_copy.contents.where(is_link=True):
            if structure.parent_concept in concept_copies:
                structure._parent_concept = concept_copies[structure.parent_concept]
        sub_frames = bubble_chamber.new_set()
        space_copies = {input_space: input_space_copy, output_space: output_space_copy}
        for sub_frame in self.sub_frames:
            (sub_frame_input_space, sub_frame_output_space) = (
                (sub_frame.input_space, sub_frame.output_space)
                if sub_frame.input_space.parent_concept == input_space.parent_concept
                else (sub_frame.output_space, sub_frame.input_space)
            )
            sub_frame_instance = sub_frame.instantiate(
                input_space=sub_frame_input_space,
                parent_id=parent_id,
                bubble_chamber=bubble_chamber,
                conceptual_spaces_map=conceptual_spaces_map,
                input_copies=input_copies,
                output_copies=output_copies,
            )
            sub_frames.add(sub_frame_instance)
            space_copies[sub_frame_input_space] = sub_frame_instance.input_space
            space_copies[sub_frame_output_space] = sub_frame_instance.output_space
        for original, copy in input_copies.items():
            if original.parent_space in space_copies:
                if original.is_link_or_node:
                    copy._parent_space = space_copies[original.parent_space]
                elif original.is_node:
                    copy.parent_space = space_copies[original.parent_space]
                elif original.is_label or original.is_relation:
                    copy._parent_space = space_copies[original.parent_space]
        for original, copy in output_copies.items():
            if original.parent_space in space_copies:
                if original.is_node:
                    copy.parent_space = space_copies[original.parent_space]
                elif original.is_label or original.is_relation:
                    copy._parent_space = space_copies[original.parent_space]
        interspatial_links = StructureSet.union(
            bubble_chamber.new_set(
                *[
                    relation.copy(
                        bubble_chamber=bubble_chamber,
                        start=input_copies[relation.start]
                        if relation.start in input_copies
                        else output_copies[relation.start],
                        end=input_copies[relation.end]
                        if relation.end in input_copies
                        else output_copies[relation.end],
                    )
                    for relation in self.interspatial_links.where(is_relation=True)
                ]
            ),
            bubble_chamber.new_set(
                *[
                    label.copy(
                        bubble_chamber=bubble_chamber,
                        start=input_copies[label.start]
                        if label.start in input_copies
                        else output_copies[label.start],
                    )
                    for label in self.interspatial_links.where(is_label=True)
                ]
            ),
        )
        for link in interspatial_links:
            if link.parent_concept in concept_copies:
                link._parent_concept = concept_copies[link.parent_concept]
        new_frame = bubble_chamber.new_frame(
            parent_id=parent_id,
            name=ID.new_frame_instance(self.name),
            parent_concept=self.parent_concept,
            parent_frame=self,
            sub_frames=sub_frames,
            concepts=concepts,
            interspatial_links=interspatial_links,
            input_space=input_space_copy,
            output_space=output_space_copy,
            is_sub_frame=self.is_sub_frame,
            depth=self.depth,
        )
        for abstract_space, conceptual_space in conceptual_spaces_map:
            new_frame.specify_space(abstract_space, conceptual_space)
        return new_frame

    def __repr__(self) -> str:
        return f"<{self.structure_id} {self.name}>"
