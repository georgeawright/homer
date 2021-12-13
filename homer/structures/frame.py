from __future__ import annotations

from homer.errors import MissingStructureError
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Frame(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: "Concept",
        parent_frame: Frame,
        sub_frames: StructureCollection,
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
        self.input_space = input_space
        self.output_space = output_space
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
        def specify_space(parent_space, abstract_space, specified_space):
            parent_space.conceptual_spaces.remove(abstract_space)
            parent_space.conceptual_spaces.add(specified_space)
            for item in parent_space.contents:
                try:
                    item.location_in_space(abstract_space).space = specified_space
                    specified_space.add(item)
                except MissingStructureError:
                    pass

        output_space = (
            self.output_space if input_space == self.input_space else self.input_space
        )
        input_space, _ = input_space.copy(
            bubble_chamber=bubble_chamber, parent_id=parent_id
        )
        for conceptual_space in input_space.conceptual_spaces.where(is_slot=True):
            specified_space = conceptual_spaces_map[conceptual_space]
            specify_space(input_space, conceptual_space, specified_space)
        output_space, _ = output_space.copy(
            bubble_chamber=bubble_chamber, parent_id=parent_id
        )
        for conceptual_space in output_space.conceptual_spaces.where(is_slot=True):
            specified_space = conceptual_spaces_map[conceptual_space]
            specify_space(output_space, conceptual_space, specified_space)
        return bubble_chamber.new_frame(
            parent_id=parent_id,
            name=self.name,
            parent_concept=self.parent_concept,
            parent_frame=self,
            input_space=input_space,
            output_space=output_space,
        )

    def copy(self, **kwargs: dict) -> Frame:
        raise NotImplementedError
