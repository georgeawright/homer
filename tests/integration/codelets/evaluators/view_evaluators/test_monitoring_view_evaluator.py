import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators.view_evaluators import MonitoringViewEvaluator
from homer.codelets.selectors.view_selectors import MonitoringViewSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import Frame, WorkingSpace
from homer.structures.views import MonitoringView


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    view_concept = Concept(
        Mock(),
        Mock(),
        "view-monitoring",
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
def input_concept():
    concept = Concept("", "", "input", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    return concept


@pytest.fixture
def text_concept():
    concept = Concept("", "", "text", Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    return concept


@pytest.fixture
def interpretation_concept():
    concept = Concept(
        "", "", "interpretation", Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    return concept


@pytest.fixture
def raw_input_space(input_concept):
    space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        input_concept,
        Mock(),
        Mock(),
        StructureCollection({Mock()}),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def raw_input_item(raw_input_space):
    item = Chunk(
        "",
        "",
        [Location([], raw_input_space)],
        StructureCollection(),
        raw_input_space,
        Mock(),
        is_raw=True,
    )
    raw_input_space.add(item)
    return item


@pytest.fixture
def good_view(
    bubble_chamber,
    text_concept,
    interpretation_concept,
    raw_input_space,
    raw_input_item,
):
    text_space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        text_concept,
        Mock(),
        Mock(),
        StructureCollection(),
        1,
        [],
        [],
    )
    interpretation_space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        interpretation_concept,
        Mock(),
        Mock(),
        StructureCollection(),
        0,
        [],
        [],
    )
    interpretation_member = Chunk(
        "",
        "",
        [Location([], interpretation_space)],
        StructureCollection({Mock()}),
        Mock(),
        Mock(),
    )
    interpretation_space.add(interpretation_member)
    member_1 = Correspondence(
        Mock(),
        Mock(),
        raw_input_item,
        interpretation_member,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        1.0,
    )
    view = MonitoringView(
        Mock(),
        Mock(),
        Location([], Mock()),
        StructureCollection({member_1}),
        StructureCollection({text_space, interpretation_space, raw_input_space}),
        Mock(),
        0.5,
    )
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def bad_view(
    bubble_chamber,
    text_concept,
    interpretation_concept,
    raw_input_space,
    raw_input_item,
):
    text_space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        text_concept,
        Mock(),
        Mock(),
        StructureCollection(),
        1,
        [],
        [],
    )
    interpretation_space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        interpretation_concept,
        Mock(),
        Mock(),
        StructureCollection({Mock()}),
        Mock(),
        Mock(),
        Mock(),
    )
    member_1 = Correspondence(
        Mock(),
        Mock(),
        raw_input_item,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        0.3,
    )
    view = MonitoringView(
        Mock(),
        Mock(),
        Location([], Mock()),
        StructureCollection({member_1}),
        StructureCollection({text_space, interpretation_space, raw_input_space}),
        Mock(),
        0.5,
    )
    bubble_chamber.views.add(view)
    return view


def test_increases_quality_of_good_view(bubble_chamber, good_view):
    original_quality = good_view.quality
    parent_id = ""
    urgency = 1.0
    evaluator = MonitoringViewEvaluator.spawn(
        parent_id, bubble_chamber, StructureCollection({good_view}), urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_view.quality > original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], MonitoringViewSelector)


def test_decreases_quality_of_bad_view(bubble_chamber, bad_view):
    original_quality = bad_view.quality
    parent_id = ""
    urgency = 1.0
    evaluator = MonitoringViewEvaluator.spawn(
        parent_id, bubble_chamber, StructureCollection({bad_view}), urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_view.quality < original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], MonitoringViewSelector)
