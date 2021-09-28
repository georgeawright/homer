import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.view_builders import MonitoringViewBuilder
from homer.codelets.suggesters.view_suggesters import MonitoringViewSuggester
from homer.structure_collection import StructureCollection
from homer.structures.spaces import Frame
from homer.structures.views import MonitoringView
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.has_view.return_value = False
    chamber.concepts = {
        "suggest": Mock(),
        "view-monitoring": Mock(),
        "text": Mock(),
        "interpretation": Mock(),
    }
    chamber.monitoring_views = StructureCollection()
    return chamber


@pytest.fixture
def input_space(bubble_chamber):
    space = Mock()
    space.activation = 1.0
    bubble_chamber.spaces = {"input": space}
    return space


@pytest.fixture
def interpretation_space():
    space = Mock()
    space.activation = 1.0
    return space


def test_gives_high_confidence_for_highly_activated_spaces(
    bubble_chamber, input_space, interpretation_space
):
    view_suggester = MonitoringViewSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        {"input_spaces": StructureCollection({input_space, interpretation_space})},
        Mock(),
    )
    result = view_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert view_suggester.confidence == 1
    assert len(view_suggester.child_codelets) == 1
    assert isinstance(view_suggester.child_codelets[0], MonitoringViewBuilder)


def test_gives_low_confidence_for_low_activated_spaces(
    bubble_chamber, input_space, interpretation_space
):
    input_space.activation = 0.0
    interpretation_space.activation = 0.0
    view_suggester = MonitoringViewSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        {"input_spaces": StructureCollection({input_space, interpretation_space})},
        1.0,
    )
    result = view_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert view_suggester.confidence == 0
    assert len(view_suggester.child_codelets) == 1
    assert isinstance(view_suggester.child_codelets[0], MonitoringViewBuilder)
