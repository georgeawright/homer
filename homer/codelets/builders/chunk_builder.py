from __future__ import annotations
import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.links import Relation
from homer.structures.nodes import Chunk
from homer.tools import average_vector, project_item_into_space


class ChunkBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: StructureCollection,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self._target_structures = target_structures
        self.second_target_chunk = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators import ChunkEvaluator

        return ChunkEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_chunk,
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        return not self.bubble_chamber.has_chunk(
            StructureCollection.union(
                *[self._members_from_chunk(chunk) for chunk in self.target_structures]
            )
        )

    def _process_structure(self):
        target_one = self._target_structures["target_one"]
        target_two = self._target_structures["target_two"]
        new_chunk_members = StructureCollection.union(
            self._members_from_chunk(target_one),
            self._members_from_chunk(target_two),
        )
        parent_spaces = StructureCollection.union(
            target_one.parent_spaces, target_two.parent_spaces
        )
        for parent_space in parent_spaces:
            for member in new_chunk_members:
                if member.has_location_in_space(parent_space):
                    continue
                if parent_space.is_basic_level:
                    project_item_into_space(member, parent_space)
        locations = [
            self._get_merged_location(new_chunk_members, space)
            for space in parent_spaces
        ]
        chunk = Chunk(
            ID.new(Chunk),
            self.codelet_id,
            locations,
            new_chunk_members,
            target_one.parent_space,
            0,
        )
        for parent_space in chunk.parent_spaces:
            parent_space.add(chunk)
        activation_from_chunk_one = target_one.activation * target_one.size / chunk.size
        activation_from_chunk_two = target_two.activation * target_two.size / chunk.size
        chunk.activation = max(
            activation_from_chunk_one + activation_from_chunk_two,
            self.INITIAL_STRUCTURE_ACTIVATION,
        )
        target_one.activation = activation_from_chunk_one
        target_two.activation = activation_from_chunk_two
        for member in list(new_chunk_members.structures) + [target_one, target_two]:
            member.chunks_made_from_this_chunk.add(chunk)
        self.bubble_chamber.chunks.add(chunk)
        self.bubble_chamber.logger.log(chunk)
        self.bubble_chamber.logger.log(target_one)
        self.bubble_chamber.logger.log(target_two)
        self._copy_across_links(target_one, chunk)
        self._copy_across_links(target_two, chunk)
        self.child_structures = StructureCollection({chunk})

    def _members_from_chunk(self, chunk):
        return StructureCollection({chunk}) if chunk.size == 1 else chunk.members

    def _copy_across_links(self, original_chunk, new_chunk):
        views = StructureCollection()
        for correspondence in original_chunk.correspondences:
            for view in self.bubble_chamber.views:
                if correspondence in view.members:
                    views.add(view)
        for view in views:
            new_view = view.copy(
                bubble_chamber=self.bubble_chamber,
                parent_id=self.codelet_id,
                original_structure=original_chunk,
                replacement_structure=new_chunk,
            )
            self.bubble_chamber.logger.log(new_view.output_space)
            for structure in new_view.output_space.contents:
                self.bubble_chamber.logger.log(structure)
            for correspondence in new_view.members:
                self.bubble_chamber.logger.log(correspondence)
            self.bubble_chamber.logger.log(new_view)
        for label in original_chunk.labels:
            if new_chunk.has_label(label.parent_concept):
                existing_label = new_chunk.label_of_type(label.parent_concept)
                existing_label.quality = statistics.fmean(
                    [existing_label.quality, label.quality]
                )
            else:
                new_label = label.copy(start=new_chunk, parent_id=self.codelet_id)
                new_chunk.links_out.add(new_label)
                new_label.parent_space.add(new_label)
        for relation in original_chunk.links_out.of_type(Relation):
            if new_chunk.has_relation(
                relation.parent_space,
                relation.parent_concept,
                new_chunk,
                relation.end,
            ):
                existing_relation = new_chunk.relation_in_space_of_type_with(
                    relation.parent_space,
                    relation.parent_concept,
                    new_chunk,
                    relation.end,
                )
                existing_relation.quality = statistics.fmean(
                    [existing_relation.quality, relation.quality]
                )
            else:
                new_relation = relation.copy(start=new_chunk, parent_id=self.codelet_id)
                new_chunk.links_out.add(new_relation)
                new_relation.parent_space.add(new_relation)
        for relation in original_chunk.links_in.of_type(Relation):
            if new_chunk.has_relation(
                relation.parent_space,
                relation.parent_concept,
                relation.start,
                new_chunk,
            ):
                existing_relation = new_chunk.relation_in_space_of_type_with(
                    relation.parent_space,
                    relation.parent_concept,
                    relation.start,
                    new_chunk,
                )
                existing_relation.quality = statistics.fmean(
                    [existing_relation.quality, relation.quality]
                )
            else:
                new_relation = relation.copy(end=new_chunk, parent_id=self.codelet_id)
                new_chunk.links_in.add(new_relation)
                new_relation.parent_space.add(new_relation)
        for correspondence in original_chunk.correspondences:
            other_arg = correspondence.arguments.get(exclude=[new_chunk])
            if new_chunk.has_correspondence(
                correspondence.conceptual_space,
                correspondence.parent_concept,
                other_arg,
            ):
                existing_correspondence = new_chunk.correspondences.where(
                    conceptual_space=correspondence.conceptual_space,
                    parent_concept=correspondence.parent_concept,
                    arguments=StructureCollection({new_chunk, other_arg}),
                ).get()
                existing_correspondence.quality = statistics.fmean(
                    [existing_correspondence.quality, correspondence.quality]
                )
            else:
                new_correspondence = correspondence.copy(
                    old_arg=original_chunk, new_arg=new_chunk, parent_id=self.codelet_id
                )
                new_correspondence.start.links_in.add(new_correspondence)
                new_correspondence.start.links_out.add(new_correspondence)
                new_correspondence.end.links_in.add(new_correspondence)
                new_correspondence.end.links_out.add(new_correspondence)
                for location in new_correspondence.locations:
                    location.space.add(new_correspondence)
        for link in new_chunk.links:
            self.bubble_chamber.add_to_collections(link)
            self.bubble_chamber.logger.log(link)

    def _get_merged_location(self, chunks: StructureCollection, space: Space):
        coordinates = []
        for chunk in chunks:
            for coords in chunk.location_in_space(space).coordinates:
                coordinates.append(coords)
        return Location(coordinates, space)

    def _fizzle(self):
        pass

    def _fail(self):
        pass
