from unittest.mock import Mock

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk


def test_size_no_members():
    chunk = Chunk(
        Mock(), Mock(), Mock(), Mock(), StructureCollection(), Mock(), Mock(), Mock()
    )
    assert chunk.size == 1


def test_size_recursive():
    size = 10
    members = StructureCollection()
    for _ in range(size):
        members.add(
            Chunk(
                Mock(),
                Mock(),
                Mock(),
                Mock(),
                StructureCollection(),
                Mock(),
                Mock(),
                Mock(),
            )
        )
    chunk = Chunk(Mock(), Mock(), Mock(), Mock(), members, Mock(), Mock(), Mock())
    assert size == chunk.size


def test_nearby():
    space_1 = Mock()
    space_1_object = Chunk(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    space_1.contents.near.return_value = StructureCollection({space_1_object})
    space_1_location = Mock()
    space_1_location.space = space_1
    space_2 = Mock()
    space_2_object = Chunk(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    space_2.contents.near.return_value = StructureCollection(
        {space_2_object, space_1_object}
    )
    space_2_location = Mock()
    space_2_location.space = space_2
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        space_1_location,
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({space_1}),
    )
    chunk.parent_spaces.add(space_2)
    chunk.locations.append(space_2_location)
    assert space_1_object in chunk.nearby()
    assert space_2_object in chunk.nearby()
    assert space_1_object in chunk.nearby(space_1)
    assert space_2_object not in chunk.nearby(space_1)
    assert space_1_object in chunk.nearby(space_2)
    assert space_2_object in chunk.nearby(space_2)


def test_add_member():
    current_member = Mock()
    current_member.value = [1]
    current_member.location = Location([1, 1], Mock())
    current_member.size = 1
    mutual_neighbour = Mock()
    new_members_neighbour = Mock()
    new_member = Chunk(
        Mock(),
        Mock(),
        [2],
        Location([1, 2], Mock()),
        StructureCollection(),
        StructureCollection({mutual_neighbour, new_members_neighbour}),
        Mock(),
        Mock(),
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        current_member.value,
        current_member.location,
        StructureCollection({current_member}),
        StructureCollection({mutual_neighbour, new_member}),
        Mock(),
        Mock(),
    )
    chunk.add_member(new_member)
    assert [1.5] == chunk.value
    assert [1, 1.5] == chunk.location.coordinates
    assert 2 == chunk.size
    assert new_member in chunk.members
    assert new_member not in chunk.neighbours
    assert new_members_neighbour in chunk.neighbours
