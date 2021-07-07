import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators.phrase_evaluators import PhraseProjectionEvaluator
from homer.codelets.selectors.phrase_selectors import PhraseProjectionSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Phrase, Rule, Word
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.structures.spaces.frames import Template
from homer.structures.views import DiscourseView
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
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(phrase_concept)
    evaluate_concept = Concept(
        Mock(),
        Mock(),
        "evaluate",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(evaluate_concept)
    relation = Relation(Mock(), Mock(), phrase_concept, evaluate_concept, None, None, 1)
    phrase_concept.links_out.add(relation)
    evaluate_concept.links_in.add(relation)
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
    text_space = ConceptualSpace(
        "", "", "text", text_concept, [], StructureCollection(), 1, [], []
    )
    chamber.conceptual_spaces.add(text_space)
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
def frame_phrase_1(template):
    chunk = Chunk(
        "", "", [Location([[None]], template)], StructureCollection(), template, 1.0
    )
    label = Label("", "", chunk, Mock(), template, 1.0)
    phrase = Phrase("", "", chunk, label, 1.0)
    return phrase


@pytest.fixture
def frame_phrase_2(template):
    chunk = Chunk(
        "", "", [Location([[None]], template)], StructureCollection(), template, 1.0
    )
    label = Label("", "", chunk, Mock(), template, 1.0)
    phrase = Phrase("", "", chunk, label, 1.0)
    return phrase


@pytest.fixture
def good_phrase_projection(
    bubble_chamber,
    parent_view,
    original_phrase,
    frame_phrase_1,
    input_space,
    template,
):
    input_to_frame_correspondence = Correspondence(
        "",
        "",
        original_phrase,
        frame_phrase_1,
        input_space,
        template,
        [
            original_phrase.location_in_space(input_space),
            frame_phrase_1.location_in_space(template),
        ],
        bubble_chamber.concepts["same"],
        bubble_chamber.spaces["text"],
        parent_view,
        1.0,
    )
    original_phrase.links_out.add(input_to_frame_correspondence)
    original_phrase.links_in.add(input_to_frame_correspondence)
    frame_phrase_1.links_out.add(input_to_frame_correspondence)
    frame_phrase_1.links_in.add(input_to_frame_correspondence)
    parent_view.members.add(input_to_frame_correspondence)
    word_1, word_2 = Mock(), Mock()
    chunk = Chunk(
        "",
        "",
        [Location([[0], [1]], parent_view.output_space)],
        StructureCollection({word_1, word_2}),
        parent_view.output_space,
        0.0,
    )
    label = Label("", "", chunk, Mock(), parent_view.output_space, 1.0)
    root = Concept("", "", "a", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    rule = Rule("", "", "a --> b c", Mock(), root, Mock(), Mock())
    output_phrase = Phrase(
        "", "", chunk, label, 0.0, left_branch=word_1, right_branch=word_2, rule=rule
    )
    input_to_output_correspondence = Correspondence(
        "",
        "",
        original_phrase,
        output_phrase,
        input_space,
        parent_view.output_space,
        [
            original_phrase.location_in_space(input_space),
            output_phrase.location_in_space(parent_view.output_space),
        ],
        bubble_chamber.concepts["same"],
        bubble_chamber.spaces["text"],
        parent_view,
        0.0,
    )
    frame_to_output_correspondence = Correspondence(
        "",
        "",
        frame_phrase_1,
        output_phrase,
        input_space,
        parent_view.output_space,
        [
            frame_phrase_1.location_in_space(template),
            output_phrase.location_in_space(parent_view.output_space),
        ],
        bubble_chamber.concepts["same"],
        bubble_chamber.spaces["text"],
        parent_view,
        0.0,
    )
    return StructureCollection(
        {output_phrase, input_to_output_correspondence, frame_to_output_correspondence}
    )


@pytest.fixture
def bad_phrase_projection(
    bubble_chamber,
    parent_view,
    original_phrase,
    frame_phrase_2,
    input_space,
    template,
):
    input_to_frame_correspondence = Correspondence(
        "",
        "",
        original_phrase,
        frame_phrase_2,
        input_space,
        template,
        [
            original_phrase.location_in_space(input_space),
            frame_phrase_2.location_in_space(template),
        ],
        bubble_chamber.concepts["same"],
        bubble_chamber.spaces["text"],
        parent_view,
        0.0,
    )
    original_phrase.links_out.add(input_to_frame_correspondence)
    original_phrase.links_in.add(input_to_frame_correspondence)
    frame_phrase_2.links_out.add(input_to_frame_correspondence)
    frame_phrase_2.links_in.add(input_to_frame_correspondence)
    parent_view.members.add(input_to_frame_correspondence)
    word_1, word_2 = Mock(), Mock()
    chunk = Chunk(
        "",
        "",
        [Location([[0], [1]], parent_view.output_space)],
        StructureCollection({word_1, word_2}),
        parent_view.output_space,
        0.0,
    )
    label = Label("", "", chunk, Mock(), parent_view.output_space, 1.0)
    root = Concept("", "", "a", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    rule = Rule("", "", "a --> b c", Mock(), root, Mock(), Mock())
    output_phrase = Phrase(
        "", "", chunk, label, 0.0, left_branch=word_1, right_branch=word_2, rule=rule
    )
    input_to_output_correspondence = Correspondence(
        "",
        "",
        original_phrase,
        output_phrase,
        input_space,
        parent_view.output_space,
        [
            original_phrase.location_in_space(input_space),
            output_phrase.location_in_space(parent_view.output_space),
        ],
        bubble_chamber.concepts["same"],
        bubble_chamber.spaces["text"],
        parent_view,
        0.0,
    )
    frame_to_output_correspondence = Correspondence(
        "",
        "",
        frame_phrase_2,
        output_phrase,
        input_space,
        parent_view.output_space,
        [
            frame_phrase_2.location_in_space(template),
            output_phrase.location_in_space(parent_view.output_space),
        ],
        bubble_chamber.concepts["same"],
        bubble_chamber.spaces["text"],
        parent_view,
        0.0,
    )
    return StructureCollection(
        {output_phrase, input_to_output_correspondence, frame_to_output_correspondence}
    )


def test_increases_quality_of_good_phrase_projection(
    bubble_chamber, good_phrase_projection
):
    original_quality = good_phrase_projection.get_random().quality
    parent_id = ""
    urgency = 1.0
    evaluator = PhraseProjectionEvaluator.spawn(
        parent_id, bubble_chamber, good_phrase_projection, urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    for structure in good_phrase_projection:
        assert structure.quality > original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], PhraseProjectionSelector)


def test_decreases_quality_of_bad_phrase_projection(
    bubble_chamber, bad_phrase_projection
):
    original_quality = bad_phrase_projection.get_random().quality
    parent_id = ""
    urgency = 1.0
    evaluator = PhraseProjectionEvaluator.spawn(
        parent_id, bubble_chamber, bad_phrase_projection, urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    for structure in bad_phrase_projection:
        assert structure.quality <= original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], PhraseProjectionSelector)
