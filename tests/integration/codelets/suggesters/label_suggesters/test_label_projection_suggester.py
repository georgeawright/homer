import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders.label_builders import LabelProjectionBuilder
from homer.codelets.suggesters.label_suggesters import LabelProjectionSuggester
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Word
from homer.structures.spaces import ConceptualSpace, WorkingSpace
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
    label_concept = Concept(
        "", "", "label", Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    chamber.concepts.add(label_concept)
    relation = Relation(Mock(), Mock(), label_concept, suggest_concept, None, None, 1)
    label_concept.links_out.add(relation)
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
def label_concepts_space(bubble_chamber):
    space = ConceptualSpace(
        "",
        "",
        "label concepts",
        Mock(),
        [Location([], label_concepts_space)],
        StructureCollection(),
        1,
        [],
        [],
    )
    bubble_chamber.conceptual_spaces.add(space)
    return space


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
def location_concept():
    concept = Concept(
        "",
        "",
        "location",
        Location([], Mock()),
        Mock(),
        "value",
        Mock(),
        Mock(),
        Mock(),
    )
    return concept


@pytest.fixture
def location_space(label_concepts_space, location_concept):
    space = ConceptualSpace(
        "",
        "",
        "location",
        location_concept,
        [Location([], label_concepts_space)],
        StructureCollection(),
        1,
        [],
        [],
    )
    label_concepts_space.add(space)
    return space


@pytest.fixture
def south_concept(bubble_chamber, location_space):
    concept = Concept(
        "",
        "",
        "south",
        Location([[5, 2]], location_space),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def noun_concept(bubble_chamber):
    concept = Concept("", "", "noun", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def noun(text_space, noun_concept, south_concept):
    lexeme = Lexeme("", "", Mock(), {WordForm.HEADWORD: "south"}, Mock())
    south_link = Relation("", "", south_concept, lexeme, Mock(), None, 1)
    lexeme.links_in.add(south_link)
    south_concept.links_out.add(south_link)
    word = Word(
        "",
        "",
        lexeme,
        WordForm.HEADWORD,
        Location([[1]], text_space),
        text_space,
        Mock(),
    )
    text_space.add(word)
    noun_label = Label("", "", word, noun_concept, text_space, 1.0)
    word.links_out.add(noun_label)
    return word


@pytest.fixture
def target_chunk(interpretation_space, noun, target_view):
    chunk = Chunk(
        "chunk",
        "",
        Mock(),
        [Location([], interpretation_space)],
        Mock(),
        interpretation_space,
        1,
    )
    interpretation_space.add(chunk)
    correspondence_to_noun = Correspondence(
        "correspondence",
        "",
        noun,
        chunk,
        noun.parent_space,
        chunk.parent_space,
        [],
        Mock(),
        Mock(),
        target_view,
        1,
    )
    chunk.links_out.add(correspondence_to_noun)
    chunk.links_in.add(correspondence_to_noun)
    noun.links_out.add(correspondence_to_noun)
    noun.links_in.add(correspondence_to_noun)
    return chunk


@pytest.fixture
def temperature_concept():
    concept = Concept(
        "",
        "",
        "",
        Location([], Mock()),
        Mock(),
        "value",
        Mock(),
        Mock(),
        Mock(),
    )
    return concept


@pytest.fixture
def temperature_space(label_concepts_space, temperature_concept):
    space = ConceptualSpace(
        "",
        "",
        "temperature",
        temperature_concept,
        [Location([], label_concepts_space)],
        StructureCollection(),
        1,
        [],
        [],
    )
    label_concepts_space.add(space)
    return space


@pytest.fixture
def hot_concept(bubble_chamber, temperature_space):
    concept = Concept(
        "",
        "",
        "hot",
        Location([[20]], temperature_space),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def adj_concept(bubble_chamber):
    concept = Concept("", "", "jj", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def target_word(text_space, noun, adj_concept, hot_concept):
    lexeme = Lexeme("", "", Mock(), {WordForm.HEADWORD: "hot"}, Mock())
    hot_link = Relation("", "", hot_concept, lexeme, Mock(), None, 1)
    lexeme.links_in.add(hot_link)
    hot_concept.links_out.add(hot_link)
    word = Word(
        "", "", lexeme, WordForm.HEADWORD, Location([[3]], text_space), Mock(), Mock()
    )
    text_space.add(word)
    adj_label = Label("", "", word, adj_concept, text_space, 1.0)
    word.links_out.add(adj_label)
    nsubj_concept = Mock()
    nsubj_concept.name = "nsubj"
    nsubj_link = Relation("", "", word, noun, nsubj_concept, text_space, 1)
    word.links_out.add(nsubj_link)
    noun.links_in.add(nsubj_link)
    return word


def test_gives_high_confidence_for_word_and_spawns_follow_up(
    bubble_chamber, target_view, target_chunk, noun, target_word
):
    parent_id = ""
    urgency = 1.0
    suggester = LabelProjectionSuggester.spawn(
        parent_id,
        bubble_chamber,
        {
            "target_view": target_view,
            "target_chunk": target_chunk,
            "target_word": target_word,
        },
        urgency,
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert isinstance(suggester.child_codelets[0], LabelProjectionBuilder)
