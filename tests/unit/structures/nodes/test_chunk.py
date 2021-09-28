import pytest
from unittest.mock import Mock

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Chunk


def test_size_no_members():
    chunk = Chunk(Mock(), Mock(), Mock(), StructureCollection(), Mock(), Mock(), Mock())
    assert chunk.size == 1


def test_size_recursive():
    size = 10
    members = StructureCollection()
    for _ in range(size):
        members.add(
            Chunk(Mock(), Mock(), Mock(), StructureCollection(), Mock(), Mock())
        )
    chunk = Chunk(Mock(), Mock(), Mock(), members, Mock(), Mock())
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
    )
    assert chunk.location_in_space(space_1) == space_1_location
    assert chunk.location_in_space(space_2) == space_2_location


def test_raw_members():
    raw_chunk_1 = Chunk("", "", [], StructureCollection(), Mock(), Mock(), is_raw=True)
    raw_chunk_2 = Chunk("", "", [], StructureCollection(), Mock(), Mock(), is_raw=True)
    raw_chunk_3 = Chunk("", "", [], StructureCollection(), Mock(), Mock(), is_raw=True)
    raw_chunk_4 = Chunk("", "", [], StructureCollection(), Mock(), Mock(), is_raw=True)

    left_chunk = Chunk(
        "", "", [], StructureCollection({raw_chunk_1, raw_chunk_2}), Mock(), Mock()
    )
    right_chunk = Chunk(
        "", "", [], StructureCollection({raw_chunk_3, raw_chunk_4}), Mock(), Mock()
    )
    root_chunk = Chunk(
        "",
        "",
        [],
        StructureCollection({left_chunk, right_chunk}),
        Mock(),
        Mock(),
        left_branch=StructureCollection({left_chunk}),
        right_branch=StructureCollection({right_chunk}),
        rule=Mock(),
    )

    assert StructureCollection({raw_chunk_1, raw_chunk_2}) == left_chunk.raw_members
    assert StructureCollection({raw_chunk_3, raw_chunk_4}) == right_chunk.raw_members
    assert (
        StructureCollection({raw_chunk_1, raw_chunk_2, raw_chunk_3, raw_chunk_4})
        == root_chunk.raw_members
    )


def test_copy_to_location():
    parent_space = Mock()
    parent_space.is_conceptual_space = False
    conceptual_space = Mock()
    conceptual_space.is_conceptual_space = True

    contextual_location = Location([], parent_space)

    left_conceptual_location = Location([[1]], conceptual_space)
    left_locations = [contextual_location, left_conceptual_location]
    left_chunk = Chunk("", "", left_locations, StructureCollection(), parent_space, 1)

    right_conceptual_location = Location([[2]], conceptual_space)
    right_locations = [contextual_location, right_conceptual_location]
    right_chunk = Chunk("", "", right_locations, StructureCollection(), parent_space, 1)

    root_conceptual_location = Location([[1], [2]], conceptual_space)
    root_locations = [contextual_location, root_conceptual_location]
    root_chunk = Chunk(
        "",
        "",
        root_locations,
        StructureCollection({left_chunk, right_chunk}),
        parent_space,
        1,
        left_branch=StructureCollection({left_chunk}),
        right_branch=StructureCollection({right_chunk}),
        rule=Mock(),
    )

    left_chunk.super_chunks.add(root_chunk)
    right_chunk.super_chunks.add(root_chunk)

    bubble_chamber = Mock()
    bubble_chamber.chunks = StructureCollection()

    new_space = Mock()
    new_space.contents = StructureCollection()
    new_location = Location([], new_space)

    root_copy = root_chunk.copy_to_location(new_location, bubble_chamber, "")

    assert 2 == len(root_copy.members)
    assert 1 == len(root_copy.left_branch)
    assert 1 == len(root_copy.right_branch)
    assert 3 == len(new_space.contents)
    assert 3 == len(bubble_chamber.chunks)
