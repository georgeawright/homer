import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders.relation_builders import RelationProjectionBuilder
from homer.codelets.suggesters.relation_suggesters import RelationProjectionSuggester
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
    relation_concept = Concept(
        "", "", "relation", Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    chamber.concepts.add(relation_concept)
    relation = Relation(
        Mock(), Mock(), relation_concept, suggest_concept, None, None, 1
    )
    relation_concept.links_out.add(relation)
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
def relational_concepts_space(bubble_chamber):
    space = ConceptualSpace(
        "",
        "",
        "relational concepts",
        Mock(),
        [Location([], Mock())],
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
def noun_concept(bubble_chamber):
    concept = Concept("", "", "noun", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def south_word(text_space, noun_concept):
    lexeme = Lexeme("", "", Mock(), {WordForm.HEADWORD: "south"}, Mock())
    word = Word(
        "",
        "",
        lexeme,
        WordForm.HEADWORD,
        Location([[6]], text_space),
        text_space,
        Mock(),
    )
    text_space.add(word)
    noun_label = Label("", "", word, noun_concept, text_space, 1.0)
    word.links_out.add(noun_label)
    return word


@pytest.fixture
def target_structure_one(interpretation_space, south_word, target_view):
    chunk = Chunk(
        "chunk",
        "",
        [Location([], interpretation_space)],
        Mock(),
        interpretation_space,
        1,
    )
    interpretation_space.add(chunk)
    correspondence_to_noun = Correspondence(
        "correspondence",
        "",
        south_word,
        chunk,
        south_word.parent_space,
        chunk.parent_space,
        [],
        Mock(),
        Mock(),
        target_view,
        1,
    )
    chunk.links_out.add(correspondence_to_noun)
    chunk.links_in.add(correspondence_to_noun)
    south_word.links_out.add(correspondence_to_noun)
    south_word.links_in.add(correspondence_to_noun)
    return chunk


@pytest.fixture
def north_word(text_space, noun_concept):
    lexeme = Lexeme("", "", Mock(), {WordForm.HEADWORD: "north"}, Mock())
    word = Word(
        "",
        "",
        lexeme,
        WordForm.HEADWORD,
        Location([[9]], text_space),
        text_space,
        Mock(),
    )
    text_space.add(word)
    noun_label = Label("", "", word, noun_concept, text_space, 1.0)
    word.links_out.add(noun_label)
    return word


@pytest.fixture
def target_structure_two(interpretation_space, north_word, target_view):
    chunk = Chunk(
        "chunk",
        "",
        [Location([], interpretation_space)],
        Mock(),
        interpretation_space,
        1,
    )
    interpretation_space.add(chunk)
    correspondence_to_noun = Correspondence(
        "correspondence",
        "",
        north_word,
        chunk,
        north_word.parent_space,
        chunk.parent_space,
        [],
        Mock(),
        Mock(),
        target_view,
        1,
    )
    chunk.links_out.add(correspondence_to_noun)
    chunk.links_in.add(correspondence_to_noun)
    north_word.links_out.add(correspondence_to_noun)
    north_word.links_in.add(correspondence_to_noun)
    return chunk


@pytest.fixture
def temperature_concept():
    concept = Concept(
        "",
        "",
        "",
        [Location([], Mock())],
        Mock(),
        "value",
        Mock(),
        Mock(),
        Mock(),
    )
    return concept


@pytest.fixture
def temperature_space(temperature_concept):
    space = ConceptualSpace(
        "",
        "",
        "temperature",
        temperature_concept,
        [Location([], Mock())],
        StructureCollection(),
        1,
        [],
        [],
    )
    return space


@pytest.fixture
def hot_concept(bubble_chamber, temperature_space):
    concept = Concept(
        "",
        "",
        "hot",
        [Location([[20]], temperature_space)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def more_less_concept(bubble_chamber):
    concept = Concept(
        "",
        "",
        "more-less",
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def more_less_space(more_less_concept, relational_concepts_space, bubble_chamber):
    space = ConceptualSpace(
        "",
        "",
        "more less space",
        more_less_concept,
        [Location([], relational_concepts_space)],
        StructureCollection(),
        1,
        [],
        [],
    )
    relational_concepts_space.add(space)
    return space


@pytest.fixture
def more_concept(bubble_chamber, more_less_space, hot_concept):
    concept = Concept(
        "",
        "",
        "more",
        [Location([[4]], more_less_space)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    more_less_space.add(concept)
    bubble_chamber.concepts.add(concept)
    more_hot_link = Relation("", "", concept, hot_concept, Mock(), None, 1)
    more_hot_link._activation = 1
    concept.links_out.add(more_hot_link)
    hot_concept.links_in.add(more_hot_link)
    return concept


@pytest.fixture
def adj_concept(bubble_chamber):
    concept = Concept("", "", "jj", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def target_word(
    text_space, south_word, north_word, adj_concept, hot_concept, more_concept
):
    lexeme = Lexeme(
        "",
        "",
        Mock(),
        {WordForm.HEADWORD: "hot", WordForm.COMPARATIVE: "hotter"},
        Mock(),
    )
    hot_link = Relation("", "", hot_concept, lexeme, Mock(), None, 1)
    lexeme.links_in.add(hot_link)
    hot_concept.links_out.add(hot_link)
    hotter_word = Word(
        "",
        "",
        lexeme,
        WordForm.COMPARATIVE,
        Location([[3]], text_space),
        Mock(),
        Mock(),
    )
    text_space.add(hotter_word)
    in_lexeme = Lexeme("", "", Mock(), {WordForm.HEADWORD: "in"}, Mock())
    in_word = Word(
        "",
        "",
        in_lexeme,
        WordForm.HEADWORD,
        Location([[4]], text_space),
        Mock(),
        Mock(),
    )
    prep_concept = Mock()
    prep_concept.name = "prep"
    prep_link = Relation("", "", hotter_word, in_word, prep_concept, text_space, 1)
    hotter_word.links_out.add(prep_link)
    in_word.links_in.add(prep_link)
    pobj_concept = Mock()
    pobj_concept.name = "pobj"
    pobj_link = Relation("", "", in_word, south_word, pobj_concept, text_space, 1)
    in_word.links_out.add(pobj_link)
    south_word.links_in.add(pobj_link)
    dep_concept = Mock()
    dep_concept.name = "dep"
    dep_link = Relation("", "", south_word, north_word, dep_concept, text_space, 1)
    south_word.links_out.add(dep_link)
    north_word.links_in.add(dep_link)
    return hotter_word


@pytest.mark.skip
def test_gives_high_confidence_for_word_and_spawns_follow_up(
    bubble_chamber,
    target_view,
    target_structure_one,
    target_structure_two,
    south_word,
    target_word,
):
    parent_id = ""
    urgency = 1.0
    suggester = RelationProjectionSuggester.spawn(
        parent_id,
        bubble_chamber,
        {
            "target_view": target_view,
            "target_structure_one": target_structure_one,
            "target_structure_two": None,
            "target_word": target_word,
        },
        urgency,
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert isinstance(suggester.child_codelets[0], RelationProjectionBuilder)
