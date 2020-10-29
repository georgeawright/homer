from unittest.mock import Mock

from homer.structures import Chunk


def test_size_no_members():
    chunk = Chunk(Mock(), Mock(), [], Mock(), Mock(), Mock())
    assert chunk.size == 1


def test_size_recursive():
    size = 10
    member_chunk = Chunk(Mock(), Mock(), [], Mock(), Mock(), Mock())
    chunk = Chunk(
        Mock(), Mock(), [member_chunk for _ in range(size)], Mock(), Mock(), Mock()
    )
    assert size == chunk.size
