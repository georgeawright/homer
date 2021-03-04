import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors import WordSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Relation
from homer.structures.nodes import Concept, Word
from homer.structures.spaces import WorkingSpace


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
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
    word_concept = Concept(
        Mock(),
        Mock(),
        "word",
        Mock(),
        None,
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(word_concept)
    select_concept = Concept(
        Mock(),
        Mock(),
        "select",
        Mock(),
        None,
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(select_concept)
    relation = Relation(Mock(), Mock(), word_concept, select_concept, None, None, 1)
    word_concept.links_out.add(relation)
    select_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def view(bubble_chamber):
    view = View(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def good_word(view):
    word = Word(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), 1.0)
    return word


@pytest.fixture
def bad_word(view):
    word = Word(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), 0.0)
    return word


@pytest.mark.skip
def test_good_word_is_boosted(bubble_chamber, good_word):
    original_activation = good_word.activation
    parent_id = ""
    urgency = 1.0
    selector = WordSelector.spawn(parent_id, bubble_chamber, good_word, urgency)
    selector.run()
    good_word.update_activation()
    assert good_word.activation > original_activation


@pytest.mark.skip
def test_bad_word_is_not_boosted(bubble_chamber, bad_word):
    original_activation = bad_word.activation
    parent_id = ""
    urgency = 1.0
    selector = WordSelector.spawn(parent_id, bubble_chamber, bad_word, urgency)
    selector.run()
    bad_word.update_activation()
    assert bad_word.activation <= original_activation
