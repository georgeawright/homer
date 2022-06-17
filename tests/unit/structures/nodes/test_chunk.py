import pytest
from unittest.mock import Mock

from linguoplotter.location import Location
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.nodes import Chunk


def test_size_no_members(bubble_chamber):
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert chunk.size == 1


def test_size_recursive(bubble_chamber):
    size = 10
    members = bubble_chamber.new_structure_collection()
    for _ in range(size):
        members.add(
            Chunk(
                Mock(),
                Mock(),
                Mock(),
                bubble_chamber.new_structure_collection(),
                Mock(),
                Mock(),
                Mock(),
                Mock(),
                Mock(),
                Mock(),
            )
        )
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        members,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert size == chunk.size


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
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert chunk.location_in_space(space_1) == space_1_location
    assert chunk.location_in_space(space_2) == space_2_location


def test_raw_members(bubble_chamber):
    raw_chunk_1 = Chunk(
        "",
        "",
        [],
        bubble_chamber.new_structure_collection(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        is_raw=True,
    )
    raw_chunk_2 = Chunk(
        "",
        "",
        [],
        bubble_chamber.new_structure_collection(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        is_raw=True,
    )
    raw_chunk_3 = Chunk(
        "",
        "",
        [],
        bubble_chamber.new_structure_collection(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        is_raw=True,
    )
    raw_chunk_4 = Chunk(
        "",
        "",
        [],
        bubble_chamber.new_structure_collection(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        is_raw=True,
    )

    super_chunk_1 = Chunk(
        "",
        "",
        [],
        bubble_chamber.new_structure_collection(raw_chunk_1, raw_chunk_2),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    super_chunk_2 = Chunk(
        "",
        "",
        [],
        bubble_chamber.new_structure_collection(raw_chunk_3, raw_chunk_4),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )

    assert (
        bubble_chamber.new_structure_collection(raw_chunk_1, raw_chunk_2)
        == super_chunk_1.raw_members
    )
    assert (
        bubble_chamber.new_structure_collection(raw_chunk_3, raw_chunk_4)
        == super_chunk_2.raw_members
    )
