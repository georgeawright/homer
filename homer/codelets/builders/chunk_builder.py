from __future__ import annotations
import statistics

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
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
        target_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_chunk = target_chunk
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

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target = bubble_chamber.chunks.get_unhappy()
        urgency = urgency if urgency is not None else target.unhappiness
        return cls.spawn(parent_id, bubble_chamber, target, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    @property
    def target_structures(self):
        return StructureCollection({self.target_chunk, self.second_target_chunk})

    def _passes_preliminary_checks(self):
        try:
            self.second_target_chunk = self.target_chunk.nearby().get_random()
        except MissingStructureError:
            return False
        return not self.bubble_chamber.has_chunk(
            StructureCollection.union(
                self._members_from_chunk(self.target_chunk),
                self._members_from_chunk(self.second_target_chunk),
            )
        )

    def _calculate_confidence(self):
        distances = [
            space.proximity_between(self.target_chunk, self.second_target_chunk)
            for space in self.target_chunk.parent_spaces
            if space.is_basic_level
        ]
        self.confidence = 0.0 if distances == [] else fuzzy.AND(*distances)

    def _process_structure(self):
        new_chunk_members = StructureCollection.union(
            self._members_from_chunk(self.target_chunk),
            self._members_from_chunk(self.second_target_chunk),
        )
        locations = []
        parent_spaces = StructureCollection.union(
            self.target_chunk.parent_spaces, self.second_target_chunk.parent_spaces
        )
        for parent_space in parent_spaces:
            for member in new_chunk_members:
                if member.has_location_in_space(parent_space):
                    continue
                if parent_space.is_basic_level:
                    project_item_into_space(member, parent_space)
        for parent_space in parent_spaces:
            locations.append(
                self._get_average_location(new_chunk_members, space=parent_space)
            )
        chunk = Chunk(
            ID.new(Chunk),
            self.codelet_id,
            self._get_average_value(new_chunk_members),
            locations,
            new_chunk_members,
            self.target_chunk.parent_space,
            0,
        )
        activation_from_chunk_one = (
            self.target_chunk.activation * self.target_chunk.size / chunk.size
        )
        activation_from_chunk_two = (
            self.second_target_chunk.activation
            * self.second_target_chunk.size
            / chunk.size
        )
        chunk.activation = max(
            activation_from_chunk_one + activation_from_chunk_two,
            self.INITIAL_STRUCTURE_ACTIVATION,
        )
        self.target_chunk.activation = activation_from_chunk_one
        self.second_target_chunk.activation = activation_from_chunk_two
        chunk.locations = [
            self._get_average_location(chunk.members, space)
            for space in chunk.parent_spaces
        ]
        for member in list(new_chunk_members.structures) + [
            self.target_chunk,
            self.second_target_chunk,
        ]:
            member.chunks_made_from_this_chunk.add(chunk)
        self.bubble_chamber.chunks.add(chunk)
        self.bubble_chamber.logger.log(chunk)
        self.bubble_chamber.logger.log(self.target_chunk)
        self.bubble_chamber.logger.log(self.second_target_chunk)
        self._copy_across_links(self.target_chunk, chunk)
        self._copy_across_links(self.second_target_chunk, chunk)
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
            other_arg = correspondence.arguments.get_random(exclude=[new_chunk])
            if new_chunk.has_correspondence(
                correspondence.conceptual_space,
                correspondence.parent_concept,
                other_arg,
            ):
                existing_correspondence = new_chunk.correspondences.where(
                    conceptual_space=correspondence.conceptual_space,
                    parent_concept=correspondence.parent_concept,
                    arguments=StructureCollection({new_chunk, other_arg}),
                ).get_random()
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

    def _get_average_value(self, chunks: StructureCollection):
        values = []
        for chunk in chunks:
            for _ in range(chunk.size):
                values.append(chunk.value[0])
        return [average_vector(values)]

    def _get_average_location(self, chunks: StructureCollection, space: Space = None):
        if space is not None:
            locations = []
            for chunk in chunks:
                for _ in range(chunk.size):
                    locations.append(chunk.location_in_space(space))
            return Location.average(locations)
        locations = []
        for chunk in chunks:
            for _ in range(chunk.size):
                locations.append(chunk.location)
        return Location.average(locations)

    def _fizzle(self):
        self.child_codelets.append(
            self.make(self.codelet_id, self.bubble_chamber, urgency=self.urgency / 2)
        )

    def _fail(self):
        self._fizzle()
