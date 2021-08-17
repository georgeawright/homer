import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Space, View
from homer.structures.nodes import Chunk, Word
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
        StructureCollection(),
        StructureCollection({chunk}),
        StructureCollection({concept}),
        StructureCollection(),
        StructureCollection(),
        StructureCollection({label}),
        StructureCollection({relation}),
        StructureCollection(),
        StructureCollection({word}),
        StructureCollection(),
        StructureCollection(),
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
    word_form = Mock()
    lexeme = Mock()
    lexeme.forms = {word_form: Mock()}
    word = Word(
        Mock(),
        Mock(),
        lexeme,
        word_form,
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
