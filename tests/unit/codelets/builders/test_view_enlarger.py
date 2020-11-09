import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import ViewBuilder, ViewEnlarger
from homer.structure_collection import StructureCollection
from homer.structures.chunks import View


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
def existing_correspondence():
    correspondence = Mock()
    correspondence.quality = 1.0
    correspondence.common_arguments_with.return_value = StructureCollection()
    return correspondence


@pytest.fixture
def candidate_correspondence(common_space, second_target_view):
    correspondence = Mock()
    correspondence.quality = 1.0
    correspondence.common_arguments_with.return_value = StructureCollection()
    return correspondence


@pytest.fixture
def target_view(candidate_correspondence, existing_correspondence):
    view = Mock()
    view.members = StructureCollection({existing_correspondence})
    view.nearby.get_random.return_value = candidate_correspondence
    return view


def test_gets_candidate_member(bubble_chamber, target_view):
    view_enlarger = ViewEnlarger(
        Mock(), Mock(), Mock(), bubble_chamber, target_view, Mock()
    )
    assert view_enlarger.candidate_member is None
    view_enlarger.run()
    assert view_enlarger.candidate_member is not None


def test_successful_adds_to_view_and_spawns_follow_up(
    bubble_chamber, target_view, candidate_correspondence
):
    view_enlarger = ViewEnlarger(
        Mock(), Mock(), Mock(), bubble_chamber, target_view, Mock()
    )
    result = view_enlarger.run()
    assert CodeletResult.SUCCESS == result
    target_view.add_member.assert_called_with(candidate_correspondence)
    assert len(view_enlarger.child_codelets) == 1
    assert isinstance(view_enlarger.child_codelets[0], ViewEnlarger)


def test_fails_when_correspondences_are_equivalent(
    bubble_chamber, target_view, candidate_correspondence, existing_correspondence
):
    existing_correspondence.common_arguments_with.return_value = StructureCollection(
        {Mock(), Mock()}
    )
    view_enlarger = ViewEnlarger(
        Mock(), Mock(), Mock(), bubble_chamber, target_view, 1.0
    )
    result = view_enlarger.run()
    assert CodeletResult.FAIL == result
    assert view_enlarger.child_structure is None
    assert len(view_enlarger.child_codelets) == 1
    assert isinstance(view_enlarger.child_codelets[0], ViewEnlarger)


def test_fails_when_correspondences_are_not_transitive(
    bubble_chamber, target_view, candidate_correspondence, existing_correspondence
):
    common_argument = Mock()
    existing_correspondence.start = common_argument
    existing_correspondence.end.correspondences_with.return_value = (
        StructureCollection()
    )
    candidate_correspondence.start = common_argument
    existing_correspondence.common_arguments_with.return_value = StructureCollection(
        {common_argument}
    )
    view_enlarger = ViewEnlarger(
        Mock(), Mock(), Mock(), bubble_chamber, target_view, 1.0
    )
    result = view_enlarger.run()
    assert CodeletResult.FAIL == result
    assert view_enlarger.child_structure is None
    assert len(view_enlarger.child_codelets) == 1
    assert isinstance(view_enlarger.child_codelets[0], ViewEnlarger)


def test_fizzles_when_no_second_target(
    bubble_chamber, target_view, existing_correspondence
):
    target_view.nearby = StructureCollection()
    urgency = 1.0
    view_enlarger = ViewEnlarger(
        Mock(), Mock(), Mock(), bubble_chamber, target_view, urgency
    )
    result = view_enlarger.run()
    assert CodeletResult.FIZZLE == result
    assert view_enlarger.child_structure is None
    assert len(view_enlarger.child_codelets) == 1
    assert isinstance(view_enlarger.child_codelets[0], ViewEnlarger)


def test_fizzles_when_view_already_exists(bubble_chamber, target_view):
    bubble_chamber.has_view.return_value = True
    urgency = 1.0
    view_enlarger = ViewEnlarger(
        Mock(), Mock(), Mock(), bubble_chamber, target_view, urgency
    )
    result = view_enlarger.run()
    assert CodeletResult.FIZZLE == result
    assert view_enlarger.child_structure is None
    assert len(view_enlarger.child_codelets) == 1
    assert isinstance(view_enlarger.child_codelets[0], ViewEnlarger)
