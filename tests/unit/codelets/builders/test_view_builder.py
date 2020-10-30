import pytest
from unittest.mock import Mock

from homer.codelets.builders import ViewBuilder, ViewEnlarger
from homer.structure_collection import StructureCollection
from homer.structures import View


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"view": Mock()}
    chamber.has_view.return_value = False
    chamber.views.get_unhappy.return_value = Mock()
    return chamber


@pytest.fixture
def common_space():
    space = Mock()
    space.proximity_between.return_value = 1.0
    return space


@pytest.fixture
def second_target_view(common_space):
    view = Mock()
    view.neighbours = StructureCollection()
    view.parent_spaces = StructureCollection({common_space})
    return view


@pytest.fixture
def target_view(common_space, second_target_view):
    view = Mock()
    view.members = StructureCollection()
    view.neighbours = StructureCollection()
    view.parent_spaces = StructureCollection({common_space})
    view.nearby.get_random.return_value = second_target_view
    return view


@pytest.mark.skip
def test_successful_creates_view_and_spawns_follow_up(bubble_chamber, target_view):
    view_builder = ViewBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_view, Mock()
    )
    view_builder.run()
    assert isinstance(view_builder.child_structure, View)
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewEnlarger)


@pytest.mark.skip
def test_fails_when_views_are_incompatible(bubble_chamber, target_view, common_space):
    common_space.proximity_between.return_value = 0.0
    view_builder = ViewBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_view, Mock()
    )
    view_builder.run()
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)


@pytest.mark.skip
def test_fizzles_when_no_second_target(bubble_chamber, target_view):
    target_view.nearby = StructureCollection()
    urgency = 1.0
    view_builder = ViewBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_view, urgency
    )
    view_builder.run()
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)


@pytest.mark.skip
def test_fizzles_when_view_already_exists(bubble_chamber, target_view):
    bubble_chamber.has_view.return_value = True
    urgency = 1.0
    view_builder = ViewBuilder(
        Mock(), Mock(), Mock(), bubble_chamber, target_view, urgency
    )
    view_builder.run()
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)
