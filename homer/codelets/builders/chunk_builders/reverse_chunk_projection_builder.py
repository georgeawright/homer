import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ChunkBuilder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Correspondence
from homer.structures.nodes import Chunk
from homer.tools import project_item_into_space


class ReverseChunkProjectionBuilder(ChunkBuilder):
    """Projects a raw chunk into an interpretation space as
    the member of an interpretation chunk according to the
    labels and relations of that chunk."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_interpretation_chunk: Chunk,
        target_raw_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
    ):
        ChunkBuilder.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            target_interpretation_chunk,
            urgency,
        )
        self.target_view = target_view
        self.target_interpretation_chunk = target_interpretation_chunk
        self.target_raw_chunk = target_raw_chunk
        self.correspondee_to_raw_chunk = None
        self.new_chunk = None
        self.confidence = 0.0

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.chunk_evaluators import (
            ReverseChunkProjectionEvaluator,
        )

        return ReverseChunkProjectionEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_interpretation_chunk: Chunk,
        target_raw_chunk: Chunk,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_view,
            target_interpretation_chunk,
            target_raw_chunk,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.monitoring_views.get_active()
        target_interpretation_chunk = target_view.interpretation_space.contents.of_type(
            Chunk
        ).get_exigent()
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
            target_raw_chunk = (
                target_view.raw_input_space.contents.of_type(Chunk)
                .where(is_raw=True)
                .get_exigent()
            )
        else:
            target_raw_chunk = (
                target_members_raw_correspondees.get_random()
                .nearby(space=target_view.input_space)
                .of_type(Chunk)
                .where(is_raw=True)
                .get_exigent()
            )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            target_view,
            target_interpretation_chunk,
            target_raw_chunk,
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
            self.target_raw_chunk.value,
            [correspondee_location],
            StructureCollection(),
            self.target_interpretation_chunk.parent_space,
            0,
        )
        for space in self.target_interpretation_chunk.parent_spaces:
            if not space.is_basic_level:
                continue
            project_item_into_space(self.correspondee_to_raw_chunk, space)
        new_chunk_members = StructureCollection.union(
            self.target_interpretation_chunk.members,
            StructureCollection({self.correspondee_to_raw_chunk}),
        )
        locations = [
            self._get_average_location(new_chunk_members, space=parent_space)
            for parent_space in self.target_interpretation_chunk.parent_spaces
        ]
        self.new_chunk = Chunk(
            "",
            self.codelet_id,
            self._get_average_value(new_chunk_members),
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

    def _process_structure(self):
        self.correspondee_to_raw_chunk.structure_id = ID.new(Chunk)
        self.bubble_chamber.chunks.add(self.correspondee_to_raw_chunk)
        self.bubble_chamber.logger.log(self.correspondee_to_raw_chunk)
        self.new_chunk.structure_id = ID.new(Chunk)
        self.bubble_chamber.chunks.add(self.new_chunk)
        self.bubble_chamber.logger.log(self.new_chunk)
        for member in list(self.new_chunk.members.structures) + [
            self.target_interpretation_chunk
        ]:
            member.chunks_made_from_this_chunk.add(self.new_chunk)
        self._copy_across_links(self.target_interpretation_chunk, self.new_chunk)
        self.new_chunk._activation = self.target_interpretation_chunk.activation
        start = self.target_raw_chunk
        end = self.correspondee_to_raw_chunk
        correspondence = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            start=start,
            end=end,
            start_space=start.parent_space,
            end_space=end.parent_space,
            locations=[
                start.location_in_space(start.parent_space),
                end.location_in_space(end.parent_space),
            ],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=None,
            parent_view=self.target_view,
            quality=0,
        )
        start.links_out.add(correspondence)
        start.links_in.add(correspondence)
        end.links_out.add(correspondence)
        end.links_in.add(correspondence)
        self.bubble_chamber.correspondences.add(correspondence)
        self.bubble_chamber.logger.log(correspondence)
        self.child_structures = StructureCollection(
            {self.new_chunk, correspondence, self.correspondee_to_raw_chunk}
        )
