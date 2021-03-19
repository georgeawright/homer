import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators import PhraseEvaluator
from homer.codelets.selectors import PhraseSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Phrase, Rule, Word
from homer.structures.spaces import WorkingSpace
from homer.word_form import WordForm


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
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
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
    return chamber


@pytest.fixture
def text_concept():
    concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        "value",
        Mock(),
        Mock(),
        math.dist,
    )
    return concept


@pytest.fixture
def input_space(text_concept):
    space = WorkingSpace(
        Mock(),
        Mock(),
        "input",
        text_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
        is_basic_level=True,
    )
    return space


@pytest.fixture
def good_phrase(bubble_chamber, input_space):
    lexeme_1 = Lexeme(Mock(), Mock(), Mock(), {WordForm.HEADWORD: "the"}, Mock())
    lexeme_2 = Lexeme(Mock(), Mock(), Mock(), {WordForm.HEADWORD: "man"}, Mock())
    word_1 = Word(Mock(), Mock(), lexeme_1, WordForm.HEADWORD, Mock(), Mock(), 1.0)
    word_2 = Word(Mock(), Mock(), lexeme_2, WordForm.HEADWORD, Mock(), Mock(), 1.0)
    rule = Rule(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), stable_activation=1.0
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([[0], [1]], input_space)],
        StructureCollection({word_1, word_2}),
        input_space,
        1.0,
    )
    label = Label(Mock(), Mock(), chunk, Mock(), input_space, 1.0)
    phrase = Phrase(
        Mock(),
        Mock(),
        chunk,
        label,
        0.0,
        left_branch=word_1,
        right_branch=word_2,
        rule=rule,
    )
    bubble_chamber.phrases.add(phrase)
    input_space.contents.add(chunk)
    return phrase


@pytest.fixture
def bad_phrase(bubble_chamber, input_space):
    lexeme_1 = Lexeme(Mock(), Mock(), Mock(), {WordForm.HEADWORD: "the"}, Mock())
    lexeme_2 = Lexeme(Mock(), Mock(), Mock(), {WordForm.HEADWORD: "man"}, Mock())
    word_1 = Word(Mock(), Mock(), lexeme_1, WordForm.HEADWORD, Mock(), Mock(), 0.0)
    word_2 = Word(Mock(), Mock(), lexeme_2, WordForm.HEADWORD, Mock(), Mock(), 0.0)
    rule = Rule(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), stable_activation=0.0
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([[0], [1]], input_space)],
        StructureCollection({word_1, word_2}),
        input_space,
        1.0,
    )
    label = Label(Mock(), Mock(), chunk, Mock(), input_space, 1.0)
    phrase = Phrase(
        Mock(),
        Mock(),
        chunk,
        label,
        1.0,
        left_branch=word_1,
        right_branch=word_2,
        rule=rule,
    )
    bubble_chamber.phrases.add(phrase)
    input_space.contents.add(chunk)
    return phrase


def test_increases_quality_of_good_phrase(bubble_chamber, good_phrase):
    original_phrase_quality = good_phrase.quality
    parent_id = ""
    urgency = 1.0
    evaluator = PhraseEvaluator.spawn(parent_id, bubble_chamber, good_phrase, urgency)
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_phrase.quality > original_phrase_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], PhraseSelector)


def test_decreases_quality_of_bad_chunk(bubble_chamber, bad_phrase):
    original_phrase_quality = bad_phrase.quality
    parent_id = ""
    urgency = 1.0
    evaluator = PhraseEvaluator.spawn(parent_id, bubble_chamber, bad_phrase, urgency)
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_phrase.quality < original_phrase_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], PhraseSelector)
