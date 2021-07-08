import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders.chunk_builders import ChunkProjectionBuilder
from homer.codelets.suggesters.chunk_suggesters import ChunkProjectionSuggester
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Word
from homer.structures.spaces import WorkingSpace
from homer.structures.views import MonitoringView
from homer.tools import hasinstance
from homer.word_form import WordForm


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    suggest_concept = Concept(
        "", "", "suggest", Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    chamber.concepts.add(suggest_concept)
    chunk_concept = Concept(
        "", "", "chunk", Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    chamber.concepts.add(chunk_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, suggest_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    suggest_concept.links_in.add(relation)
    same_concept = Concept(
        "", "", "same", Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    chamber.concepts.add(same_concept)
    text_concept = Concept(
        "", "", "text", Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    chamber.concepts.add(text_concept)
    return chamber


@pytest.fixture
def interpretation_space():
    interpretation_concept = Mock()
    interpretation_concept.name = "interpretation"
    space = WorkingSpace(
        "",
        "",
        "interpretation",
        interpretation_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def text_space():
    text_concept = Mock()
    text_concept.name = "text"
    space = WorkingSpace(
        "",
        "",
        "text",
        text_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def target_view(bubble_chamber, interpretation_space, text_space):
    view = MonitoringView(
        "",
        "",
        Mock(),
        StructureCollection(),
        StructureCollection({interpretation_space, text_space}),
        text_space,
        Mock(),
    )
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def noun_concept(bubble_chamber):
    concept = Concept("", "", "noun", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def target_word(text_space, noun_concept):
    lexeme = Lexeme("", "", Mock(), {WordForm.HEADWORD: "south"}, Mock())
    word = Word(
        "", "", lexeme, WordForm.HEADWORD, Location([[0]], text_space), Mock(), Mock()
    )
    text_space.add(word)
    noun_label = Label("", "", word, noun_concept, text_space, 1.0)
    word.links_out.add(noun_label)
    return word


@pytest.mark.skip
def test_gives_hight_confidence_for_chunk_and_spawns_follow_up(
    bubble_chamber, target_view, target_word
):
    parent_id = ""
    urgency = 1.0
    suggester = ChunkProjectionSuggester.spawn(
        parent_id,
        bubble_chamber,
        {"target_view": target_view, "target_word": target_word},
        urgency,
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert isinstance(suggester.child_codelets[0], ChunkProjectionBuilder)
