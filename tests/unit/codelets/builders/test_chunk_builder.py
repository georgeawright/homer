import pytest
from unittest.mock import Mock

from homer.codelets.builders import ChunkBuilder, ChunkEnlarger
from homer.structure_collection import StructureCollection
from homer.structures import Chunk


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"chunk": Mock()}
    chamber.has_chunk.return_value = False
    chamber.chunks.get_unhappy.return_value = Mock()
    return chamber


@pytest.fixture
def common_space():
    space = Mock()
    space.proximity_between.return_value = 1.0
    return space


@pytest.fixture
def second_target_chunk(common_space):
    chunk = Mock()
    chunk.neighbours = StructureCollection()
    chunk.parent_spaces = StructureCollection({common_space})
    return chunk


@pytest.fixture
def target_chunk(common_space, second_target_chunk):
    chunk = Mock()
    chunk.members = StructureCollection()
    chunk.neighbours = StructureCollection()
    chunk.parent_spaces = StructureCollection({common_space})
    chunk.nearby.get_random.return_value = second_target_chunk
    return chunk


def test_successful_creates_chunk_and_spawns_follow_up(bubble_chamber, target_chunk):
    chunk_builder = ChunkBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    chunk_builder.run()
    assert isinstance(chunk_builder.child_structure, Chunk)
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkEnlarger)


def test_fails_when_chunks_are_incompatible(bubble_chamber, target_chunk, common_space):
    common_space.proximity_between.return_value = 0.0
    chunk_builder = ChunkBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    chunk_builder.run()
    assert chunk_builder.child_structure is None
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkBuilder)


def test_fizzles_in_unsuitable_conditions(bubble_chamber, target_chunk):
    target_chunk.nearby = StructureCollection()
    urgency = 1.0
    chunk_builder = ChunkBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, urgency
    )
    chunk_builder.run()
    assert chunk_builder.child_structure is None
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkBuilder)
