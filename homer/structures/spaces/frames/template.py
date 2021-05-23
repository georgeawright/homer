from __future__ import annotations
from typing import List, Union

from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Concept, Word
from homer.structures.spaces import ConceptualSpace, Frame


class Template(Frame):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        conceptual_space: ConceptualSpace,
        locations: List[Location],
        contents: StructureCollection,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Frame.__init__(
            self,
            structure_id,
            parent_id,
            name,
            parent_concept,
            conceptual_space,
            locations,
            contents,
            links_in=links_in,
            links_out=links_out,
        )
        self.is_template = True

    def __getitem__(self, index: int) -> Word:
        return self.contents.at(Location([[index]], self)).get_random()

    def copy(self, **kwargs: dict) -> Frame:
        """Requires keyword arguments 'bubble_chamber' and 'parent_id'."""
        from homer.structures.links import Relation

        bubble_chamber = kwargs["bubble_chamber"]
        parent_id = kwargs["parent_id"]
        new_space = Template(
            structure_id=ID.new(Template),
            parent_id=parent_id,
            name=self.name,
            parent_concept=self.parent_concept,
            conceptual_space=self.conceptual_space,
            locations=self.locations,
            contents=StructureCollection(),
        )
        bubble_chamber.logger.log(new_space)
        copies = {}
        sub_spaces = self.contents.where(is_space=True, is_basic_level=True)
        for space in sub_spaces:
            sub_space_copy = space.copy_without_contents(parent_id)
            sub_space_copy.locations = [Location([], new_space)]
            new_space.add(sub_space_copy)
            bubble_chamber.logger.log(sub_space_copy)
        for node in self.contents.where(is_node=True):
            new_node = node.copy(
                bubble_chamber=bubble_chamber,
                parent_id=parent_id,
                parent_space=new_space,
            )
            new_space.add(new_node)
            copies[node] = new_node
            for label in node.labels:
                new_label = label.copy(
                    start=new_node,
                    parent_space=new_space,
                    parent_id=parent_id,
                )
                new_node.links_out.add(new_label)
                new_space.add(new_label)
            for relation in node.links_out.where(is_relation=True):
                if relation.end not in copies:
                    continue
                new_end = copies[relation.end]
                new_relation = relation.copy(
                    start=new_node, end=new_end, parent_space=new_space
                )
                new_node.links_out.add(new_relation)
                new_space.add(new_relation)
            for relation in node.links_in.where(is_relation=True):
                if relation.start not in copies:
                    continue
                new_start = copies[relation.start]
                new_relation = relation.copy(
                    start=new_start, end=new_node, parent_space=new_space
                )
                new_node.links_in.add(new_relation)
                new_space.add(new_relation)
            for correspondence in node.correspondences:
                if correspondence.start_space not in [self] + list(
                    sub_spaces
                ) or correspondence.end_space not in [self] + list(sub_spaces):
                    new_correspondence = correspondence.copy(
                        old_arg=node, new_arg=new_node, parent_id=parent_id
                    )
                elif (
                    correspondence.start not in copies
                    or correspondence.end not in copies
                ):
                    continue
                else:
                    new_start = copies[correspondence.start]
                    new_end = copies[correspondence.end]
                    new_correspondence = correspondence.copy(
                        start=new_start, end=new_end, parent_id=parent_id
                    )
                new_correspondence.start.links_in.add(new_correspondence)
                new_correspondence.start.links_out.add(new_correspondence)
                new_correspondence.end.links_in.add(new_correspondence)
                new_correspondence.end.links_out.add(new_correspondence)
                new_space.add(new_correspondence)
        instance_to_type_link = Relation(
            ID.new(Relation),
            parent_id,
            start=new_space,
            end=self,
            parent_concept=None,
            parent_space=self.parent_space,
            quality=1.0,
        )
        new_space.links_out.add(instance_to_type_link)
        self.links_in.add(instance_to_type_link)
        bubble_chamber.concept_links.add(instance_to_type_link)
        bubble_chamber.logger.log(instance_to_type_link)
        return new_space
