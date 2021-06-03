import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.suggesters import ChunkSuggester
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation, corresponding_exigency
from homer.structures import Space
from homer.structures.nodes import Chunk
from homer.tools import average_vector, project_item_into_space


class ReverseChunkProjectionSuggester(ChunkSuggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        ChunkSuggester.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )
        self.target_view = None
        self.target_interpretation_chunk = None
        self.target_raw_chunk = None
        self.correspondee_to_raw_chunk = None
        self.new_chunk = None
        self.confidence = 0.0

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders.chunk_builders import ReverseChunkProjectionBuilder

        return ReverseChunkProjectionBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.monitoring_views.get(key=activation)
        target_interpretation_chunk = target_view.interpretation_space.contents.of_type(
            Chunk
        ).get(key=lambda x: -x.size)
        target_members_raw_correspondees = StructureCollection(
            {
                argument
                for member in target_interpretation_chunk.members
                for correspondence in member.correspondences
                for argument in correspondence.arguments
                if argument.parent_space != target_interpretation_chunk.parent_space
            }
        )
        if target_members_raw_correspondees.is_empty():
            target_raw_chunk = target_view.raw_input_space.contents.where(
                is_chunk=True, is_raw=True
            ).get(key=corresponding_exigency)
        else:
            target_raw_chunk = (
                target_members_raw_correspondees.get()
                .nearby(space=target_view.input_space)
                .where(is_chunk=True, is_raw=True)
                .get(key=corresponding_exigency)
            )
        urgency = (
            urgency
            if urgency is not None
            else statistics.fmean(
                [
                    target_interpretation_chunk.uncorrespondedness,
                    target_raw_chunk.uncorrespondedness,
                ]
            )
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_interpretation_chunk": target_interpretation_chunk,
                "target_raw_chunk": target_raw_chunk,
            },
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    @property
    def target_structures(self):
        return StructureCollection(
            {self.target_view, self.target_interpretation_chunk, self.target_raw_chunk}
        )

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_interpretation_chunk = self._target_structures[
            "target_interpretation_chunk"
        ]
        self.target_raw_chunk = self._target_structures["target_raw_chunk"]
        if self.target_raw_chunk.has_correspondence_to_space(
            self.target_interpretation_chunk.parent_space
        ):
            return False
        correspondee_location = Location(
            self.target_raw_chunk.location_in_space(
                self.target_raw_chunk.parent_space
            ).coordinates,
            self.target_interpretation_chunk.parent_space,
        )
        self.correspondee_to_raw_chunk = Chunk(
            "",
            self.codelet_id,
            [correspondee_location],
            StructureCollection(),
            self.target_interpretation_chunk.parent_space,
            0,
        )
        for space in self.target_interpretation_chunk.parent_spaces:
            if not space.is_basic_level:
                continue
            raw_chunk_location = self.target_raw_chunk.location_in_conceptual_space(
                space.conceptual_space
            )
            self.correspondee_to_raw_chunk.locations.append(
                Location(raw_chunk_location.coordinates, space)
            )
            space.add(self.correspondee_to_raw_chunk)
        new_chunk_members = StructureCollection.union(
            self.target_interpretation_chunk.members,
            StructureCollection({self.correspondee_to_raw_chunk}),
        )
        locations = [
            self._get_merged_location(new_chunk_members, space=parent_space)
            for parent_space in self.target_interpretation_chunk.parent_spaces
        ]
        self.new_chunk = Chunk(
            "",
            self.codelet_id,
            locations,
            new_chunk_members,
            self.target_interpretation_chunk.parent_space,
            0,
        )
        return True

    def _calculate_confidence(self):
        self.confidence = (
            statistics.fmean(
                [
                    link.parent_concept.classifier.classify(
                        start=link.start
                        if link.start != self.target_interpretation_chunk
                        else self.new_chunk,
                        end=link.end
                        if link.end != self.target_interpretation_chunk
                        else self.new_chunk,
                        concept=link.parent_concept,
                        space=link.parent_space,
                    )
                    for link in self.target_interpretation_chunk.links
                ]
            )
            if not self.target_interpretation_chunk.links.is_empty()
            else 0
        )

    def _get_merged_location(self, chunks: StructureCollection, space: Space):
        coordinates = []
        for chunk in chunks:
            for coords in chunk.location_in_space(space).coordinates:
                coordinates.append(coords)
        return Location(coordinates, space)
