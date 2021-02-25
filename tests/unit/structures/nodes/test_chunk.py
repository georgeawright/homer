import pytest
from unittest.mock import Mock

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Chunk


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
            )
        )
    chunk = Chunk(Mock(), Mock(), Mock(), Mock(), members, Mock(), Mock())
    assert size == chunk.size


def test_nearby():
    space_1 = Mock()
    space_1_object_location = Mock()
    space_1_object_location.space = space_1
    space_1_object = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [space_1_object_location],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    space_1.contents.near.return_value = StructureCollection({space_1_object})
    space_2 = Mock()
    space_2_object_location = Mock()
    space_2_object_location.space = space_2
    space_2_object = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [space_2_object_location],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    space_2.contents.near.return_value = StructureCollection(
        {space_2_object, space_1_object}
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [space_1_object_location, space_2_object_location],
        Mock(),
        Mock(),
        StructureCollection({space_1}),
    )
    assert space_1_object in chunk.nearby()
    assert space_2_object in chunk.nearby()
    assert space_1_object in chunk.nearby(space_1)
    assert space_2_object not in chunk.nearby(space_1)
    assert space_1_object in chunk.nearby(space_2)
    assert space_2_object in chunk.nearby(space_2)


def test_location_in_space():
    space_1 = Mock()
    space_1_location = Mock()
    space_1_location.space = space_1
    space_2 = Mock()
    space_2_location = Mock()
    space_2_location.space = space_2
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [space_1_location, space_2_location],
        Mock(),
        Mock(),
        StructureCollection({space_1}),
    )
    assert chunk.location_in_space(space_1) == space_1_location
    assert chunk.location_in_space(space_2) == space_2_location