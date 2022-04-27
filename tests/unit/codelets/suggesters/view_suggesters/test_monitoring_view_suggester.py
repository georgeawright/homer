import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.builders.view_builders import MonitoringViewBuilder
from linguoplotter.codelets.suggesters.view_suggesters import MonitoringViewSuggester
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import Frame
from linguoplotter.structures.views import MonitoringView
from linguoplotter.tools import hasinstance


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
    bubble_chamber.has_view.return_value = False
    view_suggester = MonitoringViewSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        {
            "input_spaces": bubble_chamber.new_structure_collection(
                input_space, interpretation_space
            )
        },
        Mock(),
    )
    result = view_suggester.run()
    assert CodeletResult.FINISH == result
    assert view_suggester.confidence == 1
    assert len(view_suggester.child_codelets) == 1
    assert isinstance(view_suggester.child_codelets[0], MonitoringViewBuilder)


def test_gives_low_confidence_for_low_activated_spaces(
    bubble_chamber, input_space, interpretation_space
):
    bubble_chamber.has_view.return_value = False
    input_space.activation = 0.0
    interpretation_space.activation = 0.0
    view_suggester = MonitoringViewSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        {
            "input_spaces": bubble_chamber.new_structure_collection(
                input_space, interpretation_space
            )
        },
        1.0,
    )
    result = view_suggester.run()
    assert CodeletResult.FINISH == result
    assert view_suggester.confidence == 0
    assert len(view_suggester.child_codelets) == 1
    assert isinstance(view_suggester.child_codelets[0], MonitoringViewBuilder)
