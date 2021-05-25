import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors.label_selectors import LabelProjectionSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Word
from homer.structures.spaces import WorkingSpace
from homer.structures.views import MonitoringView
from homer.word_form import WordForm


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    label_concept = Concept(
        Mock(),
        Mock(),
        "label",
        Mock(),
        None,
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(label_concept)
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
    relation = Relation(Mock(), Mock(), label_concept, select_concept, None, None, 1)
    label_concept.links_out.add(relation)
    select_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def view(bubble_chamber):
    interpretation_concept = Concept(
        "", "", "interpretation", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    interpretation_space = WorkingSpace(
        "", "", "", interpretation_concept, Mock(), [], StructureCollection(), 0, [], []
    )
    text_concept = Concept(
        "", "", "text", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    text_space = WorkingSpace(
        "", "", "", text_concept, Mock(), [], StructureCollection(), 0, [], []
    )
    existing_chunk = Chunk(
        "",
        "",
        Mock(),
        [Location([], interpretation_space)],
        Mock(),
        interpretation_space,
        Mock(),
    )
    interpretation_space.add(existing_chunk)
    lexeme = Lexeme("", "", "", {WordForm.HEADWORD: ""}, Mock(), Mock())
    existing_word = Word(
        "", "", lexeme, WordForm.HEADWORD, Location([], text_space), text_space, 0.0
    )
    chunk_word_correspondence = Correspondence(
        "",
        "",
        existing_word,
        existing_chunk,
        text_space,
        interpretation_space,
        [Location([], interpretation_space), Location([], text_space)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    existing_chunk.links_in.add(chunk_word_correspondence)
    existing_chunk.links_out.add(chunk_word_correspondence)
    existing_word.links_in.add(chunk_word_correspondence)
    existing_word.links_out.add(chunk_word_correspondence)
    view = MonitoringView(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({interpretation_space, text_space}),
        Mock(),
        Mock(),
    )
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def good_structures(view):
    label = Label("", "", Mock(), Mock(), Mock(), 1.0)
    correspondence = Correspondence(
        Mock(),
        Mock(),
        Mock(),
        label,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        view,
        1.0,
    )
    return StructureCollection({label, correspondence})


@pytest.fixture
def bad_structures(view):
    label = Label("", "", Mock(), Mock(), Mock(), 0.0)
    correspondence = Correspondence(
        Mock(),
        Mock(),
        Mock(),
        label,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        view,
        0.0,
    )
    return StructureCollection({label, correspondence})


def test_good_label_is_boosted(bubble_chamber, good_structures):
    good_label = good_structures.where(is_label=True).get_random()
    original_activation = good_label.activation
    parent_id = ""
    urgency = 1.0
    selector = LabelProjectionSelector.spawn(
        parent_id, bubble_chamber, good_structures, urgency
    )
    selector.run()
    good_label.update_activation()
    assert good_label.activation > original_activation


def test_bad_label_is_not_boosted(bubble_chamber, bad_structures):
    bad_label = bad_structures.where(is_label=True).get_random()
    original_activation = bad_label.activation
    parent_id = ""
    urgency = 1.0
    selector = LabelProjectionSelector.spawn(
        parent_id, bubble_chamber, bad_structures, urgency
    )
    selector.run()
    bad_label.update_activation()
    assert bad_label.activation <= original_activation
