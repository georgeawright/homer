import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import ViewBuilder
from homer.codelets.evaluators import ViewEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.chunks import View


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.has_view.return_value = False
    chamber.concepts = {"build": Mock(), "view": Mock(), "text": Mock()}
    chamber.conceptual_spaces = {"text": Mock()}
    chamber.spaces = {"top level working": Mock()}
    return chamber


@pytest.fixture
def target_view_correspondence():
    correspondence = Mock()
    correspondence.quality = 1
    correspondence.common_arguments_with.return_value = StructureCollection()
    return correspondence


@pytest.fixture
def second_target_view_correspondence():
    correspondence = Mock()
    correspondence.quality = 1
    return correspondence


@pytest.fixture
def second_target_view(second_target_view_correspondence):
    view = Mock()
    view.members = StructureCollection({second_target_view_correspondence})
    return view


@pytest.fixture
def target_view(target_view_correspondence, second_target_view):
    view = Mock()
    view.members = StructureCollection({target_view_correspondence})
    view.nearby.return_value = StructureCollection({second_target_view})
    return view


def test_gets_second_target_view(bubble_chamber, target_view):
    view_builder = ViewBuilder(Mock(), Mock(), bubble_chamber, target_view, Mock())
    assert view_builder.second_target_view is None
    view_builder.run()
    assert view_builder.second_target_view is not None


def test_successful_creates_view_and_spawns_follow_up(bubble_chamber, target_view):
    view_builder = ViewBuilder(Mock(), Mock(), bubble_chamber, target_view, Mock())
    result = view_builder.run()
    assert CodeletResult.SUCCESS == result
    assert isinstance(view_builder.child_structure, View)
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewEvaluator)


def test_fails_when_correspondences_are_equivalent(
    bubble_chamber, target_view, target_view_correspondence
):
    target_view_correspondence.common_arguments_with.return_value = StructureCollection(
        {Mock(), Mock()}
    )
    view_builder = ViewBuilder(Mock(), Mock(), bubble_chamber, target_view, Mock())
    result = view_builder.run()
    assert CodeletResult.FAIL == result
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)


def test_fails_when_correspondences_are_not_transitive(
    bubble_chamber,
    target_view,
    target_view_correspondence,
    second_target_view_correspondence,
):
    common_argument = Mock()
    target_view_correspondence.start = common_argument
    second_target_view_correspondence.start = common_argument
    target_view_correspondence.end.correspondences_with.return_value = (
        StructureCollection()
    )
    target_view_correspondence.common_arguments_with.return_value = StructureCollection(
        {common_argument}
    )
    view_builder = ViewBuilder(Mock(), Mock(), bubble_chamber, target_view, Mock())
    result = view_builder.run()
    assert CodeletResult.FAIL == result
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)


def test_fizzles_when_no_second_target(bubble_chamber, target_view):
    target_view.nearby.return_value = StructureCollection()
    urgency = 1.0
    view_builder = ViewBuilder(Mock(), Mock(), bubble_chamber, target_view, urgency)
    result = view_builder.run()
    assert CodeletResult.FIZZLE == result
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)


def test_fizzles_when_view_already_exists(bubble_chamber, target_view):
    bubble_chamber.has_view.return_value = True
    urgency = 1.0
    view_builder = ViewBuilder(Mock(), Mock(), bubble_chamber, target_view, urgency)
    result = view_builder.run()
    assert CodeletResult.FIZZLE == result
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)
