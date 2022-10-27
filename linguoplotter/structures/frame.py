from __future__ import annotations

import math

from linguoplotter import fuzzy
from linguoplotter.errors import NoLocationError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure import Structure
from linguoplotter.structure_collection import StructureCollection


class Frame(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: "Concept",
        parent_frame: Frame,
        sub_frames: StructureCollection,  # collection of frames (all slots)
        # structures have locations in frame and sub-frame spaces
        concepts: StructureCollection,
        input_space: "ContextualSpace",
        output_space: "ContextualSpace",
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        instances: StructureCollection,
        champion_labels: StructureCollection,
        champion_relations: StructureCollection,
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
        self.input_space = input_space
        self.output_space = output_space
        self.slot_values = {}
        self.instances = instances
        self._depth = depth
        self.is_sub_frame = is_sub_frame
        self.is_frame = True

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
    def slots(self) -> StructureCollection:
        return StructureCollection.union(
            self.input_space.contents.where(is_slot=True),
            self.output_space.contents.where(is_slot=True),
        )

    @property
    def items(self) -> StructureCollection:
        return StructureCollection.union(
            self.input_space.contents, self.output_space.contents
        ).where(is_correspondence=False)

    @property
    def corresponded_items(self) -> StructureCollection:
        return StructureCollection.union(
            self.input_space.contents.filter(
                lambda x: not x.correspondences.is_empty()
            ),
            self.output_space.contents.filter(
                lambda x: not x.correspondences.is_empty()
            ),
        ).where(is_correspondence=False)

    @property
    def uncorresponded_items(self) -> StructureCollection:
        return StructureCollection.union(
            self.input_space.contents.filter(
                lambda x: x.correspondences.where(end=x).is_empty()
            ),
            self.output_space.contents.filter(
                lambda x: x.parent_space != self.output_space
                and x.correspondences.where(start=x).is_empty()
            ),
        ).where(is_correspondence=False, is_link_or_node=False)

    @property
    def unprojected_items(self) -> StructureCollection:
        return self.output_space.contents.filter(
            lambda x: not x.is_correspondence
            and x.correspondences.where(start=x).is_empty()
        )

    @property
    def progenitor(self) -> Frame:
        self_progenitor = self
        while self_progenitor.parent_frame is not None:
            self_progenitor = self_progenitor.parent_frame
        return self_progenitor

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
        for item in StructureCollection.union(
            self.input_space.contents, self.output_space.contents
        ):
            if item.parent_space == abstract_space:
                item.parent_space = conceptual_space
            if item.is_relation and item.conceptual_space == abstract_space:
                item.conceptual_space = conceptual_space
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
            except NoLocationError:
                pass
        for concept in self.concepts:
            if concept.parent_space == abstract_space:
                concept.parent_space = conceptual_space
            if concept.has_location_in_space(abstract_space):
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
        concepts = bubble_chamber.new_structure_collection(
            *[new for old, new in concept_copies.items()]
        )
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
        sub_frames = bubble_chamber.new_structure_collection()
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
        new_frame = bubble_chamber.new_frame(
            parent_id=parent_id,
            name=ID.new_frame_instance(self.name),
            parent_concept=self.parent_concept,
            parent_frame=self,
            sub_frames=sub_frames,
            concepts=concepts,
            input_space=input_space_copy,
            output_space=output_space_copy,
            is_sub_frame=self.is_sub_frame,
            depth=self.depth,
        )
        for abstract_space, conceptual_space in conceptual_spaces_map:
            new_frame.specify_space(abstract_space, conceptual_space)
        return new_frame

    def spread_activation(self):
        pass

    def __repr__(self) -> str:
        return f"<{self.structure_id} {self.name}>"
