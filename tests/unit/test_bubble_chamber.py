import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.structure_collection import StructureCollection
from homer.structures import Space


def test_structures():
    chunk = Mock()
    concept = Mock()
    label = Mock()
    relation = Mock()
    word = Mock()
    bubble_chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
        StructureCollection({chunk}),
        StructureCollection({concept}),
        StructureCollection(),
        StructureCollection({label}),
        StructureCollection({relation}),
        StructureCollection(),
        StructureCollection({word}),
        StructureCollection(),
        Mock(),
    )
    assert chunk in bubble_chamber.structures
    assert concept in bubble_chamber.structures
    assert label in bubble_chamber.structures
    assert relation in bubble_chamber.structures
    assert word in bubble_chamber.structures


def test_spread_activations():
    chunk = Mock()
    concept = Mock()
    label = Mock()
    relation = Mock()
    word = Mock()
    bubble_chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
        StructureCollection({chunk}),
        StructureCollection({concept}),
        StructureCollection(),
        StructureCollection({label}),
        StructureCollection({relation}),
        StructureCollection(),
        StructureCollection({word}),
        StructureCollection(),
        Mock(),
    )
    bubble_chamber.spread_activations()
    chunk.spread_activation.assert_called()
    concept.spread_activation.assert_called()
    label.spread_activation.assert_called()
    relation.spread_activation.assert_called()
    word.spread_activation.assert_called()


def test_update_activations():
    chunk = Mock()
    concept = Mock()
    label = Mock()
    relation = Mock()
    word = Mock()
    bubble_chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
        StructureCollection({chunk}),
        StructureCollection({concept}),
        StructureCollection(),
        StructureCollection({label}),
        StructureCollection({relation}),
        StructureCollection(),
        StructureCollection({word}),
        StructureCollection(),
        Mock(),
    )
    bubble_chamber.update_activations()
    chunk.update_activation.assert_called()
    concept.update_activation.assert_called()
    label.update_activation.assert_called()
    relation.update_activation.assert_called()
    word.update_activation.assert_called()


def test_has_chunk():
    existing_chunk_members = StructureCollection({Mock(), Mock()})
    existing_chunk = Mock()
    existing_chunk.members = existing_chunk_members
    bubble_chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
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
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection({existing_view}),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    assert bubble_chamber.has_view(existing_view_members)


def test_common_parent_space_is_created_if_necessary():
    bubble_chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
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
    bubble_chamber.working_spaces.add(space_one)
    bubble_chamber.working_spaces.add(space_two)
    assert 2 == len(bubble_chamber.working_spaces)
    parent = bubble_chamber.common_parent_space(space_one, space_two)
    assert isinstance(parent, Space)
    assert parent in bubble_chamber.working_spaces
    assert 3 == len(bubble_chamber.working_spaces)
    parent = bubble_chamber.common_parent_space(space_one, space_two)
    assert 3 == len(bubble_chamber.working_spaces)
