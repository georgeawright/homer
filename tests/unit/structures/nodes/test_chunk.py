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
        Mock(),
        Mock(),
        Mock(),
        is_raw=True,
    )

    left_chunk = Chunk(
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
        Mock(),
        Mock(),
    )
    right_chunk = Chunk(
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
        Mock(),
        Mock(),
    )
    root_chunk = Chunk(
        "",
        "",
        [],
        bubble_chamber.new_structure_collection(left_chunk, right_chunk),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(left_chunk),
        bubble_chamber.new_structure_collection(right_chunk),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )

    assert (
        bubble_chamber.new_structure_collection(raw_chunk_1, raw_chunk_2)
        == left_chunk.raw_members
    )
    assert (
        bubble_chamber.new_structure_collection(raw_chunk_3, raw_chunk_4)
        == right_chunk.raw_members
    )
    assert (
        bubble_chamber.new_structure_collection(
            raw_chunk_1, raw_chunk_2, raw_chunk_3, raw_chunk_4
        )
        == root_chunk.raw_members
    )


def test_copy_to_location(bubble_chamber):
    parent_space = Mock()
    parent_space.is_conceptual_space = False
    conceptual_space = Mock()
    conceptual_space.is_conceptual_space = True

    contextual_location = Location([], parent_space)

    left_conceptual_location = Location([[1]], conceptual_space)
    left_locations = [contextual_location, left_conceptual_location]
    left_chunk = Chunk(
        "",
        "",
        left_locations,
        bubble_chamber.new_structure_collection(),
        parent_space,
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )

    right_conceptual_location = Location([[2]], conceptual_space)
    right_locations = [contextual_location, right_conceptual_location]
    right_chunk = Chunk(
        "",
        "",
        right_locations,
        bubble_chamber.new_structure_collection(),
        parent_space,
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )

    root_conceptual_location = Location([[1], [2]], conceptual_space)
    root_locations = [contextual_location, root_conceptual_location]
    root_chunk = Chunk(
        "",
        "",
        root_locations,
        bubble_chamber.new_structure_collection(left_chunk, right_chunk),
        parent_space,
        1,
        bubble_chamber.new_structure_collection(left_chunk),
        bubble_chamber.new_structure_collection(right_chunk),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )

    left_chunk.super_chunks.add(root_chunk)
    right_chunk.super_chunks.add(root_chunk)

    bubble_chamber.chunks = bubble_chamber.new_structure_collection()

    new_space = Mock()
    new_space.contents = bubble_chamber.new_structure_collection()
    new_location = Location([], new_space)

    root_copy = root_chunk.copy_to_location(new_location, bubble_chamber, "")

    assert 2 == len(root_copy.members)
    assert 1 == len(root_copy.left_branch)
    assert 1 == len(root_copy.right_branch)
    assert 3 == len(new_space.contents)
    assert 3 == len(bubble_chamber.chunks)
