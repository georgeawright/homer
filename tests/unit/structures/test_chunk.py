from unittest.mock import Mock

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk


def test_size_no_members():
    chunk = Chunk(Mock(), Mock(), StructureCollection(), Mock(), Mock(), Mock())
    assert chunk.size == 1


def test_size_recursive():
    size = 10
    members = StructureCollection()
    for _ in range(size):
        members.add(
            Chunk(Mock(), Mock(), StructureCollection(), Mock(), Mock(), Mock())
        )
    chunk = Chunk(Mock(), Mock(), members, Mock(), Mock(), Mock())
    assert size == chunk.size


def test_add_member():
    current_member = Mock()
    current_member.value = 1
    current_member.location = Location([1, 1], Mock())
    current_member.size = 1
    mutual_neighbour = Mock()
    new_members_neighbour = Mock()
    new_member = Chunk(
        2,
        Location([1, 2], Mock()),
        StructureCollection(),
        StructureCollection({mutual_neighbour, new_members_neighbour}),
        Mock(),
        Mock(),
    )
    chunk = Chunk(
        current_member.value,
        current_member.location,
        StructureCollection({current_member}),
        StructureCollection({mutual_neighbour, new_member}),
        Mock(),
        Mock(),
    )
    chunk.add_member(new_member)
    assert 1.5 == chunk.value
    assert [1, 1.5] == chunk.location.coordinates
    assert 2 == chunk.size
    assert new_member in chunk.members
    assert new_member not in chunk.neighbours
    assert new_members_neighbour in chunk.neighbours
