from __future__ import annotations
import statistics

from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Concept

from .contextual_space import ContextualSpace


class Frame(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        contents: StructureCollection,
        input_space: ContextualSpace,
        output_space: ContextualSpace,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
    ):
        quality = 1
        Space.__init__(
            self,
            structure_id,
            parent_id,
            name,
            parent_concept,
            contents,
            quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
        )
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
        self._activation = (
            statistics.fmean([structure.activation for structure in self.contents])
            if self.contents != []
            else 0.0
        )

    def instantiate(self, input_space: ContextualSpace, parent_id: str, bubble_chamber):
        output_space = (
            self.output_space if input_space == self.input_space else self.input_space
        )
        input_space, input_items_map = input_space.copy(
            bubble_chamber=bubble_chamber, parent_id=parent_id
        )
        output_space, output_items_map = output_space.copy(
            bubble_chamber=bubble_chamber, parent_id=parent_id
        )
        print(self.contents)
        copied_contents = bubble_chamber.new_structure_collection(
            *[
                correspondence.copy(
                    start=input_items_map[correspondence.start]
                    if correspondence.start in input_items_map
                    else output_items_map[correspondence.start],
                    end=output_items_map[correspondence.end]
                    if correspondence.end in output_items_map
                    else input_items_map[correspondence.end],
                    parent_id=parent_id,
                )
                for correspondence in self.contents
            ]
        )
        for correspondence in copied_contents:
            correspondence.start.links_out.add(correspondence)
            correspondence.start.links_in.add(correspondence)
            correspondence.end.links_out.add(correspondence)
            correspondence.end.links_in.add(correspondence)
            bubble_chamber.logger.log(correspondence)
        instance_frame = Frame(
            structure_id=ID.new(Frame),
            parent_id=parent_id,
            name=self.name,
            parent_concept=self.parent_concept,
            contents=copied_contents,
            input_space=input_space,
            output_space=output_space,
            links_in=bubble_chamber.new_structure_collection(),
            links_out=bubble_chamber.new_structure_collection(),
            parent_spaces=self.parent_spaces,
        )
        bubble_chamber.logger.log(instance_frame)
        return instance_frame

    def copy(self, **kwargs: dict) -> Frame:
        raise NotImplementedError
