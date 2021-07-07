import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders.phrase_builders import PhraseProjectionBuilder
from homer.codelets.suggesters.phrase_suggesters import PhraseProjectionSuggester
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Phrase, Rule, Word
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.structures.spaces.frames import Template
from homer.structures.views import DiscourseView
from homer.tools import hasinstance
from homer.word_form import WordForm


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    phrase_concept = Concept(
        Mock(),
        Mock(),
        "phrase",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(phrase_concept)
    suggest_concept = Concept(
        Mock(),
        Mock(),
        "suggest",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(suggest_concept)
    relation = Relation(Mock(), Mock(), phrase_concept, suggest_concept, None, None, 1)
    phrase_concept.links_out.add(relation)
    suggest_concept.links_in.add(relation)
    text_concept = Concept(
        Mock(),
        Mock(),
        "text",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(text_concept)
    same_concept = Concept(
        Mock(),
        Mock(),
        "same",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(same_concept)
    input_concept = Concept(
        Mock(),
        Mock(),
        "input",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(input_concept)
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
    )
    text_space = ConceptualSpace(
        "", "", "text", text_concept, [], StructureCollection(), 1, [], []
    )
    chamber.conceptual_spaces.add(text_space)
    chamber.working_spaces.add(top_level_working_space)
    return chamber


@pytest.fixture
def input_space(bubble_chamber):
    space = WorkingSpace(
        "",
        "",
        "input",
        bubble_chamber.concepts["input"],
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def template(bubble_chamber):
    template = Template(
        "",
        "",
        "template",
        bubble_chamber.concepts["text"],
        Mock(),
        [],
        StructureCollection(),
    )
    return template


@pytest.fixture
def parent_view(bubble_chamber, input_space, template):
    output_space = WorkingSpace(
        "",
        "",
        "view output",
        bubble_chamber.concepts["text"],
        Mock(),
        [],
        StructureCollection(),
        1,
        [],
        [],
    )
    view = DiscourseView(
        "",
        "",
        Mock(),
        StructureCollection(),
        StructureCollection({input_space, template}),
        output_space,
        0.0,
    )
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def word_1(input_space):
    lexeme = Lexeme("", "", "word", {WordForm.HEADWORD: "word"}, Mock())
    word = Word(
        "", "", lexeme, WordForm.HEADWORD, Location([[0]], input_space), Mock(), 0.0
    )
    return word


@pytest.fixture
def word_2(input_space):
    lexeme = Lexeme("", "", "word", {WordForm.HEADWORD: "word"}, Mock())
    word = Word(
        "", "", lexeme, WordForm.HEADWORD, Location([[1]], input_space), Mock(), 0.0
    )
    return word


@pytest.fixture
def original_phrase(word_1, word_2, input_space):
    chunk = Chunk(
        "",
        "",
        [Location([[0], [1]], input_space)],
        StructureCollection({word_1, word_2}),
        input_space,
        0.0,
    )
    label = Label("", "", chunk, Mock(), input_space, 1.0)
    root = Concept("", "", "a", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    rule = Rule("", "", "a --> b c", Mock(), root, Mock(), Mock())
    phrase = Phrase(
        "", "", chunk, label, 0, left_branch=word_1, right_branch=word_2, rule=rule
    )
    return phrase


@pytest.fixture
def frame_phrase(template):
    chunk = Chunk(
        "", "", [Location([], template)], StructureCollection(), template, 1.0
    )
    label = Label("", "", chunk, Mock(), template, 1.0)
    phrase = Phrase("", "", chunk, label, 1.0)
    return phrase


@pytest.fixture
def target_correspondence(
    bubble_chamber,
    parent_view,
    original_phrase,
    frame_phrase,
    input_space,
    template,
):
    correspondence = Correspondence(
        "",
        "",
        original_phrase,
        frame_phrase,
        input_space,
        template,
        [
            original_phrase.location_in_space(input_space),
            frame_phrase.location_in_space(template),
        ],
        bubble_chamber.concepts["same"],
        bubble_chamber.spaces["text"],
        parent_view,
        1.0,
    )
    correspondence._activation = 1.0
    parent_view.members.add(correspondence)
    return correspondence


def test_gives_high_confidence_for_compatible_phrase_and_spawns_follow_up(
    bubble_chamber, target_correspondence
):
    parent_id = ""
    urgency = 1.0
    suggester = PhraseProjectionSuggester.spawn(
        parent_id,
        bubble_chamber,
        {"target_correspondence": target_correspondence},
        urgency,
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert isinstance(suggester.child_codelets[0], PhraseProjectionBuilder)
