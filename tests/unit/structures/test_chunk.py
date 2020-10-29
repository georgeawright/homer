from unittest.mock import Mock

from homer.structures import Chunk

def test_size_no_members():
    chunk = Chunk(Mock(), Mock(), [], Mock(), Mock(), Mock())
    assert chunk.size == 1


def test_size_recursive():
    pass