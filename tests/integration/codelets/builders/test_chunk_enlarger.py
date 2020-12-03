import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder, ChunkEnlarger
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.links import Relation
from homer.structures.spaces import WorkingSpace


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    chunk_concept = Concept(
        Mock(), Mock(), "chunk", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(chunk_concept)
    build_concept = Concept(
        Mock(), Mock(), "build", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, build_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def target_chunk(bubble_chamber):
    location_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    input_space = WorkingSpace(
        Mock(), Mock(), "input", StructureCollection(), 0, location_concept
    )
    parent_spaces = StructureCollection({input_space})
    member_1 = Chunk(
        Mock(),
        Mock(),
        [10],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    member_2 = Chunk(
        Mock(),
        Mock(),
        [10],
        Location([0, 1], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        Location([0, 0], input_space),
        StructureCollection({member_1, member_2}),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    second_chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        Location([1, 1], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    bubble_chamber.chunks.add(chunk)
    bubble_chamber.chunks.add(second_chunk)
    input_space.contents.add(chunk)
    input_space.contents.add(second_chunk)
    chunk.parent_spaces.add(input_space)
    return chunk


def test_successful_adds_member_to_chunk_and_spawns_follow_up_and_same_chunk_cannot_be_recreated(
    bubble_chamber, target_chunk
):
    parent_id = ""
    urgency = 1.0

    enlarger = ChunkEnlarger.spawn(parent_id, bubble_chamber, target_chunk, urgency)
    assert 2 == target_chunk.size
    enlarger.run()
    assert CodeletResult.SUCCESS == enlarger.result
    assert 3 == target_chunk.size
    assert isinstance(enlarger.child_codelets[0], ChunkEnlarger)
    enlarger = ChunkEnlarger.spawn(parent_id, bubble_chamber, target_chunk, urgency)
    enlarger.run()
    assert CodeletResult.FIZZLE == enlarger.result
