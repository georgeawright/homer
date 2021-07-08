import pytest
from unittest.mock import Mock

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Chunk


@pytest.mark.skip
def test_size_no_members():
    chunk = Chunk(Mock(), Mock(), Mock(), StructureCollection(), Mock(), Mock(), Mock())
    assert chunk.size == 1


@pytest.mark.skip
def test_size_recursive():
    size = 10
    members = StructureCollection()
    for _ in range(size):
        members.add(
            Chunk(Mock(), Mock(), Mock(), StructureCollection(), Mock(), Mock())
        )
    chunk = Chunk(Mock(), Mock(), Mock(), members, Mock(), Mock())
    assert size == chunk.size


@pytest.mark.skip
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
        [space_1_location, space_2_location],
        Mock(),
        Mock(),
        Mock(),
    )
    assert chunk.location_in_space(space_1) == space_1_location
    assert chunk.location_in_space(space_2) == space_2_location
