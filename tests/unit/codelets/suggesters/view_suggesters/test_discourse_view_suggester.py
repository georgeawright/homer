import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.view_builders import DiscourseViewBuilder
from homer.codelets.suggesters.view_suggesters import DiscourseViewSuggester
from homer.structure_collection import StructureCollection
from homer.structures import Frame
from homer.structures.views import DiscourseView
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.loggers = {"activity": Mock(), "structure": Mock(), "errors": Mock()}
    chamber.has_view.return_value = False
    chamber.concepts = {
        "suggest": Mock(),
        "view-discourse": Mock(),
        "text": Mock(),
        "discourse": Mock(),
    }
    chamber.spaces = {"text": Mock(), "top level working": Mock(), "input": Mock()}
    chamber.views = StructureCollection()
    return chamber


@pytest.fixture
def input_space():
    space = Mock()
    space.is_frame = False
    space.activation = 1.0
    return space


@pytest.fixture
def frame():
    space = Mock()
    space.is_frame = True
    space.activation = 1.0
    return space


@pytest.mark.skip
def test_gives_high_confidence_for_highly_activated_spaces(
    bubble_chamber, input_space, frame
):
    view_suggester = DiscourseViewSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({input_space, frame}),
        Mock(),
    )
    result = view_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert view_suggester.confidence == 1
    assert len(view_suggester.child_codelets) == 1
    assert isinstance(view_suggester.child_codelets[0], DiscourseViewBuilder)


@pytest.mark.skip
def test_gives_low_confidence_for_low_activated_spaces(
    bubble_chamber, input_space, frame
):
    input_space.activation = 0.0
    frame.activation = 0.0
    view_suggester = DiscourseViewSuggester(
        Mock(), Mock(), bubble_chamber, StructureCollection({input_space, frame}), 1.0
    )
    result = view_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert view_suggester.confidence == 0
    assert len(view_suggester.child_codelets) == 1
    assert isinstance(view_suggester.child_codelets[0], DiscourseViewBuilder)
