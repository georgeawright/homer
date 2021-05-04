import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators import WordEvaluator
from homer.codelets.selectors import WordSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Word
from homer.structures.spaces import ConceptualSpace, WorkingSpace
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
    word_concept = Concept(
        Mock(),
        Mock(),
        "word",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(word_concept)
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
    relation = Relation(Mock(), Mock(), word_concept, evaluate_concept, None, None, 1)
    word_concept.links_out.add(relation)
    evaluate_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def temperature_conceptual_space(bubble_chamber):
    space = ConceptualSpace(
        Mock(),
        Mock(),
        "temperature",
        Mock(),
        [],
        StructureCollection(),
        1,
        [],
        [],
        is_basic_level=True,
    )
    bubble_chamber.conceptual_spaces.add(space)
    return space


@pytest.fixture
def temperature_input_space(temperature_conceptual_space):
    space = WorkingSpace(
        Mock(),
        Mock(),
        "temperature",
        Mock(),
        temperature_conceptual_space,
        [],
        StructureCollection(),
        1,
        [],
        [],
        is_basic_level=True,
    )
    return space


@pytest.fixture
def output_space():
    space = WorkingSpace(
        Mock(),
        Mock(),
        "ouptut",
        Mock(),
        Mock(),
        Mock(),
        StructureCollection(),
        1,
        [],
        [],
    )
    return space


@pytest.fixture
def warm_concept(bubble_chamber, temperature_conceptual_space):
    concept = Concept(
        Mock(),
        Mock(),
        "warm",
        Location([16], temperature_conceptual_space),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.concepts.add(concept)
    temperature_conceptual_space.add(concept)
    return concept


@pytest.fixture
def warm_lexeme(warm_concept):
    lexeme = Lexeme(Mock(), Mock(), "warm", {WordForm.HEADWORD: "warm"}, Mock())
    link = Relation(Mock(), Mock(), warm_concept, lexeme, None, None, 0)
    warm_concept.links_out.add(link)
    lexeme.links_in.add(link)
    return lexeme


@pytest.fixture
def good_word_correspondee(bubble_chamber, warm_concept, temperature_input_space):
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([16], temperature_input_space)],
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.chunks.add(chunk)
    label = Label(Mock(), Mock(), chunk, warm_concept, temperature_input_space, 1.0)
    chunk.links_out.add(label)
    return chunk


@pytest.fixture
def good_word(bubble_chamber, warm_lexeme, output_space, good_word_correspondee):
    word = Word(
        Mock(),
        Mock(),
        warm_lexeme,
        WordForm.HEADWORD,
        Location([0], output_space),
        output_space,
        0,
    )
    bubble_chamber.words.add(word)
    output_space.add(word)
    correspondence = Correspondence(
        Mock(),
        Mock(),
        good_word_correspondee,
        word,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    good_word_correspondee.links_in.add(correspondence)
    good_word_correspondee.links_out.add(correspondence)
    word.links_in.add(correspondence)
    word.links_out.add(correspondence)
    return word


@pytest.fixture
def bad_word_correspondee(bubble_chamber, warm_concept, temperature_input_space):
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([10], temperature_input_space)],
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.chunks.add(chunk)
    label = Label(Mock(), Mock(), chunk, warm_concept, temperature_input_space, 0.5)
    chunk.links_out.add(label)
    return chunk


@pytest.fixture
def bad_word(bubble_chamber, warm_lexeme, output_space, bad_word_correspondee):
    word = Word(
        Mock(),
        Mock(),
        warm_lexeme,
        WordForm.HEADWORD,
        Location([0], output_space),
        output_space,
        1,
    )
    bubble_chamber.words.add(word)
    output_space.add(word)
    correspondence = Correspondence(
        Mock(),
        Mock(),
        bad_word_correspondee,
        word,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    bad_word_correspondee.links_in.add(correspondence)
    bad_word_correspondee.links_out.add(correspondence)
    word.links_in.add(correspondence)
    word.links_out.add(correspondence)
    return word


def test_increases_quality_of_good_word(bubble_chamber, good_word):
    original_word_quality = good_word.quality
    parent_id = ""
    urgency = 1.0
    evaluator = WordEvaluator.spawn(
        parent_id, bubble_chamber, StructureCollection({good_word}), urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_word.quality > original_word_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], WordSelector)


def test_decreases_quality_of_bad_word(bubble_chamber, bad_word):
    original_word_quality = bad_word.quality
    parent_id = ""
    urgency = 1.0
    evaluator = WordEvaluator.spawn(
        parent_id, bubble_chamber, StructureCollection({bad_word}), urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_word.quality < original_word_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], WordSelector)
