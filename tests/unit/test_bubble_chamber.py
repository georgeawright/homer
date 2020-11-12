import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.structure_collection import StructureCollection
from homer.structures import Space


@pytest.mark.skip
def test_update_activations():
    pass


def test_has_chunk():
    existing_chunk_members = StructureCollection({Mock(), Mock()})
    existing_chunk = Mock()
    existing_chunk.members = existing_chunk_members
    bubble_chamber = BubbleChamber(
        Mock(),
        Mock(),
        StructureCollection({existing_chunk}),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    assert bubble_chamber.has_chunk(existing_chunk_members)


def test_has_view():
    existing_view_members = StructureCollection({Mock(), Mock()})
    existing_view = Mock()
    existing_view.members = existing_view_members
    bubble_chamber = BubbleChamber(
        Mock(),
        Mock(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection({existing_view}),
        StructureCollection(),
        Mock(),
    )
    assert bubble_chamber.has_view(existing_view_members)


def test_common_parent_space_is_created_if_necessary():
    bubble_chamber = BubbleChamber(
        Mock(),
        Mock(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    space_one = Mock()
    space_one.name = "one"
    space_one.parent_spaces = StructureCollection()
    space_two = Mock()
    space_two.name = "two"
    space_two.parent_spaces = StructureCollection()
    bubble_chamber.spaces.add(space_one)
    bubble_chamber.spaces.add(space_two)
    assert 2 == len(bubble_chamber.spaces)
    parent = bubble_chamber.common_parent_space(space_one, space_two)
    assert isinstance(parent, Space)
    assert parent in bubble_chamber.spaces
    assert 3 == len(bubble_chamber.spaces)
    parent = bubble_chamber.common_parent_space(space_one, space_two)
    assert 3 == len(bubble_chamber.spaces)
