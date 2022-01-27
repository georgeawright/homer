from __future__ import annotations

import math

from homer.errors import MissingStructureError
from homer.structure import Structure
from homer.structure_collection import StructureCollection

# TODO: allow frames to be defined as children of other frames with only parts overwritten
# TODO: subframes need corresponding exigency to be defined


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
        )
        self.name = name
        self._parent_concept = parent_concept
        self.parent_frame = parent_frame
        self.sub_frames = sub_frames
        self.concepts = concepts
        self.input_space = input_space
        self.output_space = output_space
        self.slot_values = {}
        self.is_frame = True

    @property
    def slots(self) -> StructureCollection:
        return StructureCollection.union(
            self.input_space.contents.where(is_slot=True),
            self.output_space.contents.where(is_slot=True),
        )

    def update_activation(self):
        raise NotImplementedError

    def instantiate(
        self,
        input_space: "ContextualSpace",
        conceptual_spaces_map: dict,
        parent_id: str,
        bubble_chamber,
    ):
        def specify_space(parent_space, abstract_space, specified_space, concepts):
            parent_space.conceptual_spaces.remove(abstract_space)
            parent_space.conceptual_spaces.add(specified_space)
            for item in parent_space.contents:
                if abstract_space.parent_concept in concepts:
                    concepts.remove(abstract_space.parent_concept)
                self.concepts.add(specified_space.parent_concept)
                if item.parent_space == abstract_space:
                    item.parent_space = specified_space
                try:
                    item.location_in_space(abstract_space).coordinates = [
                        [math.nan for _ in range(specified_space.no_of_dimensions)]
                    ]
                    item.location_in_space(abstract_space).space = specified_space
                    specified_space.add(item)
                except MissingStructureError:
                    pass

        concepts = self.concepts.copy()
        output_space = (
            self.output_space if input_space == self.input_space else self.input_space
        )
        input_space_copy, _ = input_space.copy(
            bubble_chamber=bubble_chamber, parent_id=parent_id
        )
        for conceptual_space in input_space_copy.conceptual_spaces.where(is_slot=True):
            specified_space = conceptual_spaces_map[conceptual_space]
            specify_space(input_space_copy, conceptual_space, specified_space, concepts)
        output_space_copy, _ = output_space.copy(
            bubble_chamber=bubble_chamber, parent_id=parent_id
        )
        for conceptual_space in output_space_copy.conceptual_spaces.where(is_slot=True):
            specified_space = conceptual_spaces_map[conceptual_space]
            specify_space(
                output_space_copy, conceptual_space, specified_space, concepts
            )
        sub_frames = bubble_chamber.new_structure_collection()
        for sub_frame in self.sub_frames:
            sub_frames.add(
                sub_frame.instantiate(
                    parent_id=parent_id,
                    bubble_chamber=bubble_chamber,
                    conceptual_spaces_map=conceptual_spaces_map,
                )
            )
        return bubble_chamber.new_frame(
            parent_id=parent_id,
            name=self.name,
            parent_concept=self.parent_concept,
            parent_frame=self,
            sub_frames=sub_frames,
            concepts=concepts,
            input_space=input_space,
            output_space=output_space_copy,
        )
