import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.view_builders import MonitoringViewBuilder
from homer.codelets.evaluators.view_evaluators import MonitoringViewEvaluator
from homer.structure_collection import StructureCollection
from homer.structures import Frame
from homer.structures.views import MonitoringView
from homer.tools import hasinstance


@pytest.fixture
def input_space(bubble_chamber):
    space = Mock()
    space.activation = 1.0
    bubble_chamber.spaces.add(space)
    return space


@pytest.fixture
def text_space():
    space = Mock()
    space.activation = 1.0
    return space


@pytest.fixture
def interpretation_space():
    space = Mock()
    space.activation = 1.0
    return space


@pytest.mark.skip
def test_successful_creates_view_and_spawns_follow_up(
    bubble_chamber, interpretation_space, input_space, text_space
):
    view_builder = MonitoringViewBuilder(
        Mock(),
        Mock(),
        bubble_chamber,
        {
            "input_spaces": bubble_chamber.new_structure_collection(
                input_space, interpretation_space
            ),
            "output_space": text_space,
        },
        Mock(),
    )
    result = view_builder.run()
    assert CodeletResult.SUCCESS == result
    assert hasinstance(view_builder.child_structures, MonitoringView)
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], MonitoringViewEvaluator)
