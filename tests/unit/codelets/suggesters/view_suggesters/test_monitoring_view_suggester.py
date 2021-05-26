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
    chamber.spaces = {"text": Mock(), "top level working": Mock(), "input": Mock()}
    text_space = Mock()
    text_space.contents.is_empty.return_value = False
    text_space.parent_concept = chamber.concepts["text"]
    chamber.working_spaces = StructureCollection({text_space})
    chamber.views = StructureCollection()
    return chamber


@pytest.fixture
def input_space():
    space = Mock()
    space.activation = 1.0
    return space


@pytest.fixture
def text_space():
    space = Frame(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    space.activation = 1.0
    return space


def test_gives_high_confidence_for_highly_activated_spaces(
    bubble_chamber, input_space, text_space
):
    view_suggester = MonitoringViewSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({input_space, text_space}),
        Mock(),
    )
    result = view_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert view_suggester.confidence == 1
    assert len(view_suggester.child_codelets) == 1
    assert isinstance(view_suggester.child_codelets[0], MonitoringViewBuilder)


def test_gives_low_confidence_for_low_activated_spaces(
    bubble_chamber, input_space, text_space
):
    input_space.activation = 0.0
    text_space.activation = 0.0
    view_suggester = MonitoringViewSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({input_space, text_space}),
        1.0,
    )
    result = view_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert view_suggester.confidence == 0
    assert len(view_suggester.child_codelets) == 1
    assert isinstance(view_suggester.child_codelets[0], MonitoringViewBuilder)
