import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder, ChunkEnlarger
from homer.structure_collection import StructureCollection
from homer.structures import Chunk


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"chunk": Mock(), "build": Mock()}
    chamber.has_chunk.return_value = False
    chamber.chunks.get_unhappy.return_value = Mock()
    return chamber


@pytest.fixture
def common_space():
    space = Mock()
    space.proximity_between.return_value = 1.0
    return space


@pytest.fixture
def candidate_chunk(common_space):
    chunk = Mock()
    chunk.neighbours = StructureCollection()
    chunk.parent_spaces = StructureCollection({common_space})
    return chunk


@pytest.fixture
def target_chunk(common_space, candidate_chunk):
    chunk = Mock()
    chunk.members = StructureCollection()
    chunk.neighbours = StructureCollection()
    chunk.parent_spaces = StructureCollection({common_space})
    chunk.nearby.return_value = StructureCollection({candidate_chunk})
    return chunk


def test_successful_adds_member_to_chunk_and_spawns_follow_up(
    bubble_chamber, target_chunk, candidate_chunk
):
    original_target_chunk_size = len(target_chunk.members)
    chunk_enlarger = ChunkEnlarger(Mock(), Mock(), bubble_chamber, target_chunk, Mock())
    result = chunk_enlarger.run()
    assert CodeletResult.SUCCESS == result
    target_chunk.add_member.assert_called_with(candidate_chunk)
    assert len(chunk_enlarger.child_codelets) == 1
    assert isinstance(chunk_enlarger.child_codelets[0], ChunkEnlarger)


def test_fails_when_chunks_are_incompatible(bubble_chamber, target_chunk, common_space):
    common_space.proximity_between.return_value = 0.0
    chunk_enlarger = ChunkEnlarger(Mock(), Mock(), bubble_chamber, target_chunk, Mock())
    result = chunk_enlarger.run()
    assert CodeletResult.FAIL == result
    assert chunk_enlarger.child_structure is None
    assert len(chunk_enlarger.child_codelets) == 1
    assert isinstance(chunk_enlarger.child_codelets[0], ChunkEnlarger)


def test_fizzles_when_no_candidate_found(bubble_chamber, target_chunk):
    target_chunk.nearby.return_value = StructureCollection()
    urgency = 1.0
    chunk_enlarger = ChunkEnlarger(
        Mock(), Mock(), bubble_chamber, target_chunk, urgency
    )
    result = chunk_enlarger.run()
    assert CodeletResult.FIZZLE == result
    assert chunk_enlarger.child_structure is None
    assert len(chunk_enlarger.child_codelets) == 1
    assert isinstance(chunk_enlarger.child_codelets[0], ChunkEnlarger)


def test_fizzles_when_bigger_chunk_already_exists(bubble_chamber, target_chunk):
    bubble_chamber.has_chunk.return_value = True
    urgency = 1.0
    chunk_enlarger = ChunkEnlarger(
        Mock(), Mock(), bubble_chamber, target_chunk, urgency
    )
    result = chunk_enlarger.run()
    assert CodeletResult.FIZZLE == result
    assert chunk_enlarger.child_structure is None
    assert len(chunk_enlarger.child_codelets) == 1
    assert isinstance(chunk_enlarger.child_codelets[0], ChunkEnlarger)
