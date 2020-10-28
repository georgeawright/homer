from unittest.mock import Mock

from homer.codelets.builders import ChunkBuilder
from homer.structures import Chunk


def test_successful_creates_chunk_and_spawns_follow_up():
    bubble_chamber = Mock()
    target_chunk = Mock()
    chunk_builder = ChunkBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    chunk_builder.run()
    assert isinstance(chunk_builder.child_structure, Chunk)
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkBuilder)


def test_fails_when_chunks_are_incompatible():
    bubble_chamber = Mock()
    target_chunk = Mock()
    chunk_builder = ChunkBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    chunk_builder.run()
    assert chunk_builder.child_structure is None
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkBuilder)


def test_fizzles_in_unsuitable_conditions():
    bubble_chamber = Mock()
    target_chunk = Mock()
    chunk_builder = ChunkBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_chunk, Mock()
    )
    chunk_builder.run()
    assert chunk_builder.child_structure is None
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkBuilder)
