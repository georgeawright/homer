import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors.chunk_selectors import ChunkProjectionSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Word
from homer.structures.spaces import WorkingSpace
from homer.structures.views import MonitoringView
from homer.word_form import WordForm


@pytest.fixture
def noun_concept():
    concept = Concept(
        Mock(), Mock(), "noun", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    return concept


@pytest.fixture
def target_view(noun_concept):
    interpretation_space = Mock()
    interpretation_space.parent_concept.name = "interpretation"
    text_concept = Concept(
        Mock(), Mock(), "text", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    text_space = WorkingSpace(
        "", "", "text", text_concept, Mock(), Mock(), StructureCollection(), 0, [], []
    )
    lexeme = Lexeme("", "", "", {WordForm.HEADWORD: ""}, Mock())
    noun = Word(
        "", "", lexeme, WordForm.HEADWORD, Location([[0]], text_space), text_space, 1.0
    )
    noun_label = Label("", "", noun, noun_concept, text_space, 1.0)
    noun.links_out.add(noun_label)
    text_space.add(noun)
    view = MonitoringView(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({interpretation_space, text_space}),
        Mock(),
        Mock(),
    )
    return view


@pytest.fixture
def bubble_chamber(target_view, noun_concept):
    chamber = BubbleChamber.setup(Mock())
    chamber.concepts.add(noun_concept)
    chamber.views.add(target_view)
    chunk_concept = Concept(
        Mock(),
        Mock(),
        "chunk",
        Mock(),
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(chunk_concept)
    select_concept = Concept(
        Mock(),
        Mock(),
        "select",
        Mock(),
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(select_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, select_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    select_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def target_space():
    space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def chunk_members():
    member_1 = Mock()
    member_1.size = 1
    member_2 = Mock()
    member_2.size = 1
    members = StructureCollection({member_1, member_2})
    return members


@pytest.fixture
def good_chunk(target_space, chunk_members):
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([[0, 0]], target_space)],
        chunk_members,
        Mock(),
        1.0,
    )
    chunk._activation = 0.0
    target_space.contents.add(chunk)
    return chunk


@pytest.fixture
def bad_chunk(target_space, chunk_members):
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([[0, 1]], target_space)],
        chunk_members,
        Mock(),
        0.0,
    )
    chunk._activation = 1.0
    target_space.contents.add(chunk)
    return chunk


def test_good_chunk_is_boosted_bad_chunk_is_decayed(
    bubble_chamber, good_chunk, bad_chunk
):
    original_good_chunk_activation = good_chunk.activation
    original_bad_chunk_activation = bad_chunk.activation
    parent_id = ""
    champion = bad_chunk
    urgency = 1.0
    selector = ChunkProjectionSelector.spawn(
        parent_id, bubble_chamber, StructureCollection({champion}), urgency
    )
    selector.run()
    good_chunk.update_activation()
    bad_chunk.update_activation()
    assert good_chunk.activation > original_good_chunk_activation
    assert bad_chunk.activation < original_bad_chunk_activation
