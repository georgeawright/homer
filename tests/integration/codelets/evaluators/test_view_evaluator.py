import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators import ViewEvaluator
from homer.codelets.selectors import ViewSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Correspondence, Relation
from homer.structures.nodes import Concept
from homer.structures.spaces import WorkingSpace


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
        Mock(),
    )
    view_concept = Concept(
        Mock(),
        Mock(),
        "view",
        Mock(),
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(view_concept)
    evaluate_concept = Concept(
        Mock(),
        Mock(),
        "evaluate",
        Mock(),
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(evaluate_concept)
    relation = Relation(Mock(), Mock(), view_concept, evaluate_concept, None, None, 1)
    view_concept.links_out.add(relation)
    evaluate_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def good_view(bubble_chamber):
    member_1 = Correspondence(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), 1.0
    )
    member_2 = Correspondence(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), 1.0
    )
    view = View(
        Mock(),
        Mock(),
        Location([], Mock()),
        StructureCollection({member_1, member_2}),
        Mock(),
        Mock(),
        0.5,
    )
    return view


@pytest.fixture
def bad_view(bubble_chamber):
    member_1 = Correspondence(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), 0.3
    )
    member_2 = Correspondence(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), 0.4
    )
    view = View(
        Mock(),
        Mock(),
        Location([], Mock()),
        StructureCollection({member_1, member_2}),
        Mock(),
        Mock(),
        0.5,
    )
    return view


def test_increases_quality_of_good_view(bubble_chamber, good_view):
    original_quality = good_view.quality
    parent_id = ""
    urgency = 1.0
    evaluator = ViewEvaluator.spawn(parent_id, bubble_chamber, good_view, urgency)
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_view.quality > original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ViewSelector)


def test_decreases_quality_of_bad_view(bubble_chamber, bad_view):
    original_quality = bad_view.quality
    parent_id = ""
    urgency = 1.0
    evaluator = ViewEvaluator.spawn(parent_id, bubble_chamber, bad_view, urgency)
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_view.quality < original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ViewSelector)
