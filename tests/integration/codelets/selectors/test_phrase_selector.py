import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors import PhraseSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Phrase, Rule, Word
from homer.structures.spaces import WorkingSpace
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
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(phrase_concept)
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
    relation = Relation(Mock(), Mock(), phrase_concept, select_concept, None, None, 1)
    phrase_concept.links_out.add(relation)
    select_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def input_space():
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
def word_1(bubble_chamber, input_space):
    lexeme_1 = Lexeme(Mock(), Mock(), Mock(), {WordForm.HEADWORD: "the"}, Mock())
    word_1 = Word(
        "word_1",
        Mock(),
        lexeme_1,
        WordForm.HEADWORD,
        Location([[0]], input_space),
        input_space,
        1.0,
    )
    bubble_chamber.words.add(word_1)
    input_space.contents.add(word_1)
    return word_1


@pytest.fixture
def word_2(bubble_chamber, input_space):
    lexeme_2 = Lexeme(Mock(), Mock(), Mock(), {WordForm.HEADWORD: "man"}, Mock())
    word_2 = Word(
        "word_2",
        Mock(),
        lexeme_2,
        WordForm.HEADWORD,
        Location([[1]], input_space),
        input_space,
        1.0,
    )
    bubble_chamber.words.add(word_2)
    input_space.contents.add(word_2)
    return word_2


@pytest.fixture
def null_phrase():
    phrase = Phrase("null_phrase", Mock(), Mock(), Mock(), Mock())
    return phrase


@pytest.fixture
def good_phrase(bubble_chamber, input_space, word_1, word_2):
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
        "good_phrase",
        Mock(),
        chunk,
        label,
        1.0,
        left_branch=word_1,
        right_branch=word_2,
        rule=rule,
    )
    bubble_chamber.phrases.add(phrase)
    input_space.contents.add(phrase)
    return phrase


@pytest.fixture
def bad_phrase(bubble_chamber, input_space, word_2, null_phrase):
    rule = Rule(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), stable_activation=1.0
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([[1]], input_space)],
        StructureCollection({word_2}),
        input_space,
        1.0,
    )
    label = Label(Mock(), Mock(), chunk, Mock(), input_space, 1.0)
    phrase = Phrase(
        "bad_phrase",
        Mock(),
        chunk,
        label,
        0.0,
        left_branch=word_2,
        right_branch=null_phrase,
        rule=rule,
    )
    bubble_chamber.phrases.add(phrase)
    input_space.contents.add(chunk)
    return phrase


def test_good_phrase_is_boosted_bad_phrase_is_decayed(
    bubble_chamber, good_phrase, bad_phrase
):
    original_good_phrase_activation = good_phrase.activation
    original_bad_phrase_activation = bad_phrase.activation
    parent_id = ""
    champion = bad_phrase
    urgency = 1.0
    selector = PhraseSelector.spawn(
        parent_id, bubble_chamber, StructureCollection({champion}), urgency
    )
    selector.run()
    good_phrase.update_activation()
    bad_phrase.update_activation()
    assert good_phrase.activation > original_good_phrase_activation
    assert bad_phrase.activation < original_bad_phrase_activation
