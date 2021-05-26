import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import ProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators.relation_evaluators import RelationProjectionEvaluator
from homer.codelets.selectors.relation_selectors import RelationProjectionSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Word
from homer.structures.spaces import WorkingSpace
from homer.word_form import WordForm


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    relation_concept = Concept(
        Mock(),
        Mock(),
        "relation",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(relation_concept)
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
    relation = Relation(
        Mock(), Mock(), relation_concept, evaluate_concept, None, None, 1
    )
    relation_concept.links_out.add(relation)
    evaluate_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def good_relation_and_correspondence(bubble_chamber):
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
    relation = Relation("", "", Mock(), Mock(), Mock(), Mock(), 0.0)
    correspondence = Correspondence(
        "", "", word, relation, Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), 0.0
    )
    return StructureCollection({relation, correspondence})


@pytest.fixture
def bad_relation_and_correspondence(bubble_chamber):
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
    relation = Relation("", "", Mock(), Mock(), Mock(), Mock(), 1.0)
    correspondence = Correspondence(
        "", "", word, relation, Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), 1.0
    )
    return StructureCollection({relation, correspondence})


def test_increases_quality_of_good_relation(
    bubble_chamber, good_relation_and_correspondence
):
    original_quality = good_relation_and_correspondence.get_random().quality
    parent_id = ""
    urgency = 1.0
    evaluator = RelationProjectionEvaluator.spawn(
        parent_id, bubble_chamber, good_relation_and_correspondence, urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_relation_and_correspondence.pop().quality > original_quality
    assert good_relation_and_correspondence.pop().quality > original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], RelationProjectionSelector)


def test_decreases_quality_of_bad_relation(
    bubble_chamber, bad_relation_and_correspondence
):
    original_quality = bad_relation_and_correspondence.get_random().quality
    parent_id = ""
    urgency = 1.0
    evaluator = RelationProjectionEvaluator.spawn(
        parent_id, bubble_chamber, bad_relation_and_correspondence, urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_relation_and_correspondence.pop().quality < original_quality
    assert bad_relation_and_correspondence.pop().quality < original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], RelationProjectionSelector)
