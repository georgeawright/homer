import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors.relation_selectors import RelationProjectionSelector
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
    relation_concept = Concept(
        Mock(),
        Mock(),
        "relation",
        Mock(),
        None,
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(relation_concept)
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
    relation = Relation(Mock(), Mock(), relation_concept, select_concept, None, None, 1)
    relation_concept.links_out.add(relation)
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
    potential_relating_word = Word(
        "", "", lexeme, WordForm.HEADWORD, Location([], text_space), text_space, 0.0
    )
    nsubj_concept = Concept(
        "", "", "nsubj", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    nsubj_relation = Relation(
        "", "", potential_relating_word, existing_word, nsubj_concept, text_space, 1.0
    )
    potential_relating_word.links_out.add(nsubj_relation)
    existing_word.links_in.add(nsubj_relation)
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
    relation = Relation("", "", Mock(), Mock(), Mock(), Mock(), 1.0)
    correspondence = Correspondence(
        Mock(),
        Mock(),
        Mock(),
        relation,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        view,
        1.0,
    )
    return StructureCollection({relation, correspondence})


@pytest.fixture
def bad_structures(view):
    relation = Relation("", "", Mock(), Mock(), Mock(), Mock(), 0.0)
    correspondence = Correspondence(
        Mock(),
        Mock(),
        Mock(),
        relation,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        view,
        0.0,
    )
    return StructureCollection({relation, correspondence})


def test_good_relation_is_boosted(bubble_chamber, good_structures):
    good_relation = good_structures.where(is_relation=True).get_random()
    original_activation = good_relation.activation
    parent_id = ""
    urgency = 1.0
    selector = RelationProjectionSelector.spawn(
        parent_id, bubble_chamber, good_structures, urgency
    )
    selector.run()
    good_relation.update_activation()
    assert good_relation.activation > original_activation


def test_bad_relation_is_not_boosted(bubble_chamber, bad_structures):
    bad_relation = bad_structures.where(is_relation=True).get_random()
    original_activation = bad_relation.activation
    parent_id = ""
    urgency = 1.0
    selector = RelationProjectionSelector.spawn(
        parent_id, bubble_chamber, bad_structures, urgency
    )
    selector.run()
    bad_relation.update_activation()
    assert bad_relation.activation <= original_activation
