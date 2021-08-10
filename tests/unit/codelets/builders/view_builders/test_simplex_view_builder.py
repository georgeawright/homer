import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.view_builders import SimplexViewBuilder
from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.spaces.frames import Template
from homer.structures.views import SimplexView
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.has_view.return_value = False
    chamber.concepts = {"build": Mock(), "view-simplex": Mock(), "text": Mock()}
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


def test_successful_creates_view_and_spawns_follow_up(
    bubble_chamber, input_space, frame
):
    view_builder = SimplexViewBuilder(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({input_space, frame}),
        Mock(),
    )
    result = view_builder.run()
    assert CodeletResult.SUCCESS == result
    assert hasinstance(view_builder.child_structures, SimplexView)
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], SimplexViewEvaluator)
