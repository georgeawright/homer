import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Space
from homer.structures.chunks import View, Word
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.spaces import WorkingSpace


def test_structures():
    chunk = Mock()
    concept = Mock()
    label = Mock()
    relation = Mock()
    word = Mock()
    bubble_chamber = BubbleChamber(
        StructureCollection(),
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
        StructureCollection(),
        Mock(),
    )
    assert chunk in bubble_chamber.structures
    assert concept in bubble_chamber.structures
    assert label in bubble_chamber.structures
    assert relation in bubble_chamber.structures
    assert word in bubble_chamber.structures


def test_add_to_collections():
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
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    correspondence = Correspondence(
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
    label = Label(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    relation = Relation(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    view = View(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    word = Word(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.add_to_collections(chunk)
    bubble_chamber.add_to_collections(correspondence)
    bubble_chamber.add_to_collections(label)
    bubble_chamber.add_to_collections(relation)
    bubble_chamber.add_to_collections(view)
    bubble_chamber.add_to_collections(word)
    assert chunk in bubble_chamber.chunks
    assert correspondence in bubble_chamber.correspondences
    assert label in bubble_chamber.labels
    assert relation in bubble_chamber.relations
    assert view in bubble_chamber.views
    assert word in bubble_chamber.words


def test_spread_activations():
    chunk = Mock()
    concept = Mock()
    label = Mock()
    relation = Mock()
    word = Mock()
    bubble_chamber = BubbleChamber(
        StructureCollection(),
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
        StructureCollection(),
        StructureCollection({chunk}),
        StructureCollection({concept}),
        StructureCollection(),
        StructureCollection({label}),
        StructureCollection({relation}),
        StructureCollection(),
        StructureCollection({word}),
        StructureCollection(),
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
        StructureCollection(),
        StructureCollection({existing_chunk}),
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
        StructureCollection(),
        StructureCollection({existing_view}),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    assert bubble_chamber.has_view(existing_view_members)


def test_get_super_space_is_created_if_necessary():
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
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    top_level_working_space = WorkingSpace(
        Mock(),
        Mock(),
        "top level working",
        None,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
        0,
    )
    space_one = WorkingSpace(
        Mock(),
        Mock(),
        "one",
        None,
        Mock(),
        [Location([], top_level_working_space)],
        Mock(),
        1,
        [],
        [],
        0,
    )
    space_two = WorkingSpace(
        Mock(),
        Mock(),
        "two",
        None,
        Mock(),
        [Location([], top_level_working_space)],
        Mock(),
        1,
        [],
        [],
        0,
    )
    bubble_chamber.working_spaces.add(top_level_working_space)
    bubble_chamber.working_spaces.add(space_one)
    bubble_chamber.working_spaces.add(space_two)
    assert 3 == len(bubble_chamber.working_spaces)
    parent = bubble_chamber.get_super_space(space_one, space_two)
    assert isinstance(parent, WorkingSpace)
    assert parent in bubble_chamber.working_spaces
    assert 4 == len(bubble_chamber.working_spaces)
    parent = bubble_chamber.get_super_space(space_one, space_two)
    assert 4 == len(bubble_chamber.working_spaces)
