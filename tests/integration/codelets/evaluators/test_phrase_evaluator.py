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
def det_concept():
    return Mock()


@pytest.fixture
def noun_concept():
    return Mock()


@pytest.fixture
def the_lexeme():
    return Lexeme(Mock(), Mock(), Mock(), {WordForm.HEADWORD: "the"}, Mock())


@pytest.fixture
def man_lexeme():
    return Lexeme(Mock(), Mock(), Mock(), {WordForm.HEADWORD: "man"}, Mock())


@pytest.fixture
def the_word(the_lexeme, input_space, det_concept):
    word = Word(
        Mock(),
        Mock(),
        the_lexeme,
        WordForm.HEADWORD,
        Location([[0]], input_space),
        Mock(),
        1.0,
    )
    word_label = Label(Mock(), Mock(), word, det_concept, input_space, 1.0)
    word.links_out.add(word_label)
    return word


@pytest.fixture
def man_word(man_lexeme, input_space, noun_concept):
    word = Word(
        Mock(),
        Mock(),
        man_lexeme,
        WordForm.HEADWORD,
        Location([[1]], input_space),
        Mock(),
        1.0,
    )
    word_label = Label(Mock(), Mock(), word, noun_concept, input_space, 1.0)
    word.links_out.add(word_label)
    return word


@pytest.fixture
def good_phrase(
    bubble_chamber, input_space, det_concept, noun_concept, the_word, man_word
):
    rule = Rule(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        det_concept,
        noun_concept,
        stable_activation=1.0,
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        [Location([[0], [1]], input_space)],
        StructureCollection({the_word, man_word}),
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
        left_branch=the_word,
        right_branch=man_word,
        rule=rule,
    )
    bubble_chamber.phrases.add(phrase)
    input_space.contents.add(chunk)
    return phrase


@pytest.fixture
def bad_phrase(
    bubble_chamber, input_space, det_concept, noun_concept, the_word, man_word
):
    the_word.label_of_type(det_concept).quality = 0
    man_word.label_of_type(noun_concept).quality = 0
    rule = Rule(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        det_concept,
        noun_concept,
        stable_activation=0.0,
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        [Location([[0], [1]], input_space)],
        StructureCollection({the_word, man_word}),
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
        left_branch=the_word,
        right_branch=man_word,
        rule=rule,
    )
    bubble_chamber.phrases.add(phrase)
    input_space.contents.add(chunk)
    return phrase


@pytest.mark.skip
def test_increases_quality_of_good_phrase(bubble_chamber, good_phrase):
    original_phrase_quality = good_phrase.quality
    parent_id = ""
    urgency = 1.0
    evaluator = PhraseEvaluator.spawn(
        parent_id, bubble_chamber, StructureCollection({good_phrase}), urgency
    )
    evaluator.run()
    good_phrase.update_activation()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_phrase.quality > original_phrase_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], PhraseSelector)


@pytest.mark.skip
def test_decreases_quality_of_bad_chunk(bubble_chamber, bad_phrase):
    original_phrase_quality = bad_phrase.quality
    parent_id = ""
    urgency = 1.0
    evaluator = PhraseEvaluator.spawn(
        parent_id, bubble_chamber, StructureCollection({bad_phrase}), urgency
    )
    evaluator.run()
    bad_phrase.update_activation()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_phrase.quality < original_phrase_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], PhraseSelector)
