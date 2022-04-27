import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.builders.view_builders import DiscourseViewBuilder
from linguoplotter.codelets.evaluators.view_evaluators import DiscourseViewEvaluator
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import Frame
from linguoplotter.structures.views import DiscourseView
from linguoplotter.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.has_view.return_value = False
    chamber.concepts = {
        "build": Mock(),
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
def test_successful_creates_view_and_spawns_follow_up(
    bubble_chamber, input_space, frame
):
    view_builder = DiscourseViewBuilder(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({input_space, frame}),
        Mock(),
    )
    result = view_builder.run()
    assert CodeletResult.SUCCESS == result
    assert hasinstance(view_builder.child_structures, DiscourseView)
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], DiscourseViewEvaluator)
