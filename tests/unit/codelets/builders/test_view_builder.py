import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import ViewBuilder, ViewEnlarger
from homer.structure_collection import StructureCollection
from homer.structures.chunks import View


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"view": Mock(), "text": Mock()}
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
def second_target_correspondence():
    correspondence = Mock()
    correspondence.quality = 1.0
    return correspondence


@pytest.fixture
def target_correspondence(
    common_space, second_target_view, second_target_correspondence
):
    correspondence = Mock()
    correspondence.quality = 1.0
    nearby_correspondences = StructureCollection({second_target_correspondence})
    correspondence.nearby.return_value = nearby_correspondences
    correspondence.common_arguments_with.return_value = StructureCollection()
    return correspondence


def test_gets_second_target_correspondence(bubble_chamber, target_correspondence):
    view_builder = ViewBuilder(
        Mock(), Mock(), bubble_chamber, target_correspondence, Mock()
    )
    assert view_builder.second_target_correspondence is None
    view_builder.run()
    assert view_builder.second_target_correspondence is not None


def test_successful_creates_view_and_spawns_follow_up(
    bubble_chamber, target_correspondence
):
    view_builder = ViewBuilder(
        Mock(), Mock(), bubble_chamber, target_correspondence, Mock()
    )
    result = view_builder.run()
    assert CodeletResult.SUCCESS == result
    assert isinstance(view_builder.child_structure, View)
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewEnlarger)


def test_fails_when_correspondences_are_equivalent(
    bubble_chamber, target_correspondence
):
    target_correspondence.common_arguments_with.return_value = StructureCollection(
        {Mock(), Mock()}
    )
    view_builder = ViewBuilder(
        Mock(), Mock(), bubble_chamber, target_correspondence, Mock()
    )
    result = view_builder.run()
    assert CodeletResult.FAIL == result
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)


def test_fails_when_correspondences_are_not_transitive(
    bubble_chamber, target_correspondence, second_target_correspondence
):
    common_argument = Mock()
    target_correspondence.start = common_argument
    second_target_correspondence.start = common_argument
    target_correspondence.end.correspondences_with.return_value = StructureCollection()
    target_correspondence.common_arguments_with.return_value = StructureCollection(
        {common_argument}
    )
    view_builder = ViewBuilder(
        Mock(), Mock(), bubble_chamber, target_correspondence, Mock()
    )
    result = view_builder.run()
    assert CodeletResult.FAIL == result
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)


def test_fizzles_when_no_second_target(bubble_chamber, target_correspondence):
    target_correspondence.nearby.return_value = StructureCollection()
    urgency = 1.0
    view_builder = ViewBuilder(
        Mock(), Mock(), bubble_chamber, target_correspondence, urgency
    )
    result = view_builder.run()
    assert CodeletResult.FIZZLE == result
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)


def test_fizzles_when_view_already_exists(bubble_chamber, target_correspondence):
    bubble_chamber.has_view.return_value = True
    urgency = 1.0
    view_builder = ViewBuilder(
        Mock(), Mock(), bubble_chamber, target_correspondence, urgency
    )
    result = view_builder.run()
    assert CodeletResult.FIZZLE == result
    assert view_builder.child_structure is None
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], ViewBuilder)
