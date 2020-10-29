from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures import Chunk


def test_size_no_members():
    chunk = Chunk(Mock(), Mock(), StructureCollection(), Mock(), Mock())
    assert chunk.size == 1


def test_size_recursive():
    size = 10
    members = StructureCollection()
    for _ in range(size):
        members.add(Chunk(Mock(), Mock(), StructureCollection(), Mock(), Mock()))
    chunk = Chunk(Mock(), Mock(), members, Mock(), Mock())
    assert size == chunk.size
