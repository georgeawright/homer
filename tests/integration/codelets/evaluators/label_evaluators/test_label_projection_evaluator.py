import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import ProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators.label_evaluators import LabelProjectionEvaluator
from homer.codelets.selectors.label_selectors import LabelProjectionSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Word
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
    label_concept = Concept(
        Mock(),
        Mock(),
        "label",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(label_concept)
    evaluate_concept = Concept(
        Mock(),
        Mock(),
        "evaluate",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(evaluate_concept)
    relation = Relation(Mock(), Mock(), label_concept, evaluate_concept, None, None, 1)
    label_concept.links_out.add(relation)
    evaluate_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def good_label_and_correspondence(bubble_chamber):
    lexeme = Lexeme("", "", "", {WordForm.HEADWORD: ""}, Mock())
    word = Word(
        "",
        "",
        lexeme,
        WordForm.HEADWORD,
        Mock(),
        Mock(),
        1.0,
    )
    label = Label("", "", Mock(), Mock(), Mock(), 0.0)
    correspondence = Correspondence(
        "", "", word, label, Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), 0.0
    )
    return StructureCollection({label, correspondence})


@pytest.fixture
def bad_label_and_correspondence(bubble_chamber):
    lexeme = Lexeme("", "", "", {WordForm.HEADWORD: ""}, Mock())
    word = Word(
        "",
        "",
        lexeme,
        WordForm.HEADWORD,
        Mock(),
        Mock(),
        0.0,
    )
    label = Label("", "", Mock(), Mock(), Mock(), 1.0)
    correspondence = Correspondence(
        "", "", word, label, Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), 1.0
    )
    return StructureCollection({label, correspondence})


def test_increases_quality_of_good_label(bubble_chamber, good_label_and_correspondence):
    original_quality = good_label_and_correspondence.get_random().quality
    parent_id = ""
    urgency = 1.0
    evaluator = LabelProjectionEvaluator.spawn(
        parent_id, bubble_chamber, good_label_and_correspondence, urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_label_and_correspondence.pop().quality > original_quality
    assert good_label_and_correspondence.pop().quality > original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], LabelProjectionSelector)


def test_decreases_quality_of_bad_label(bubble_chamber, bad_label_and_correspondence):
    original_quality = bad_label_and_correspondence.get_random().quality
    parent_id = ""
    urgency = 1.0
    evaluator = LabelProjectionEvaluator.spawn(
        parent_id, bubble_chamber, bad_label_and_correspondence, urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_label_and_correspondence.pop().quality < original_quality
    assert bad_label_and_correspondence.pop().quality < original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], LabelProjectionSelector)
