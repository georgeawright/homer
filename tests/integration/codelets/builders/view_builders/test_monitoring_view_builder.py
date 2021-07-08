import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders.view_builders import MonitoringViewBuilder
from homer.codelets.evaluators.view_evaluators import MonitoringViewEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Concept
from homer.structures.spaces import Frame, WorkingSpace
from homer.structures.views import MonitoringView
from homer.tools import hasinstance


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
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(view_concept)
    build_concept = Concept(
        Mock(),
        Mock(),
        "build",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), view_concept, build_concept, None, None, 1)
    view_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    text_concept = Concept(
        Mock(),
        Mock(),
        "text",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(text_concept)
    interpretation_concept = Concept(
        Mock(),
        Mock(),
        "interpretation",
        Mock(),
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(interpretation_concept)
    top_level_working_space = WorkingSpace(
        Mock(),
        Mock(),
        "top level working",
        Mock(),
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    chamber.working_spaces.add(top_level_working_space)
    return chamber


@pytest.fixture
def input_space(bubble_chamber):
    space = WorkingSpace(
        Mock(), Mock(), "input", Mock(), Mock(), [], StructureCollection(), 0, [], []
    )
    space._activation = 1.0
    bubble_chamber.working_spaces.add(space)
    return space


@pytest.fixture
def text_space(bubble_chamber):
    space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.concepts["text"],
        Mock(),
        [],
        StructureCollection({Mock()}),
        1,
        [],
        [],
    )
    space._activation = 1.0
    bubble_chamber.working_spaces.add(space)
    return space


@pytest.mark.skip
def test_successful_creates_view_and_spawns_follow_up_and_same_view_cannot_be_recreated(
    bubble_chamber,
    input_space,
    text_space,
):
    parent_id = ""
    urgency = 1.0
    target_spaces = StructureCollection({input_space, text_space})
    builder = MonitoringViewBuilder.spawn(
        parent_id, bubble_chamber, target_spaces, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert hasinstance(builder.child_structures, MonitoringView)
    assert isinstance(builder.child_codelets[0], MonitoringViewEvaluator)
    builder = MonitoringViewBuilder.spawn(
        parent_id, bubble_chamber, target_spaces, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
