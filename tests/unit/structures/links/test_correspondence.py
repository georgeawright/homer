import pytest
from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence


def test_copy():
    start_space = Mock()
    start_space.parent_concept = Mock()
    end_space = Mock()
    end_space.parent_concept = Mock()
    start_location = Mock()
    start_location.coordinates = [1, 1]
    start_location.space = start_space
    end_location = Mock()
    end_location.coordinates = [1, 1]
    end_location.space = end_space
    old_start = Mock()
    old_start.location_in_space.return_value = start_location
    old_start.locations = [start_location]
    old_end = Mock()
    old_end.location_in_space.return_value = end_location
    old_end.locations = [end_location]
    new_start = Mock()
    new_start.location_in_space.return_value = start_location
    new_start.locations = [start_location]
    new_end = Mock()
    new_end.location_in_space.return_value = end_location
    new_end.locations = [end_location]
    parent_id = "id"
    location = Mock()
    location.space.sub_spaces = [start_space, end_space]
    correspondence = Correspondence(
        Mock(),
        Mock(),
        old_start,
        old_end,
        location,
        start_space,
        end_space,
        Mock(),
        Mock(),
        Mock(),
    )
    copy = correspondence.copy(
        old_arg=old_start, new_arg=new_start, parent_id=parent_id
    )
    assert correspondence.start == old_start
    assert correspondence.end == old_end
    assert copy.start == new_start
    assert copy.end == old_end
    assert copy.parent_id == parent_id
    copy = correspondence.copy(old_arg=old_end, new_arg=new_end, parent_id=parent_id)
    assert correspondence.start == old_start
    assert correspondence.end == old_end
    assert copy.start == old_start
    assert copy.end == new_end
    assert copy.parent_id == parent_id


def test_nearby():
    start = Mock()
    start.correspondences = StructureCollection({Mock()})
    end = Mock()
    end.correspondences = StructureCollection({Mock()})
    parent_space = Mock()
    parent_space.contents = StructureCollection({Mock()})
    location = Mock()
    location.space = parent_space
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        location,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    parent_space.contents.add(correspondence)
    neighbours = correspondence.nearby()
    assert 3 == len(neighbours)
    assert correspondence not in neighbours


@pytest.mark.skip
def test_get_slot_argument_returns_slot():
    location = Mock()
    slot = Slot(Mock(), Mock(), Mock(), locations=[location])
    non_slot = Mock()
    correspondence = Correspondence(
        Mock(),
        Mock(),
        slot,
        non_slot,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert slot == correspondence.get_slot_argument()
    correspondence = Correspondence(
        Mock(),
        Mock(),
        non_slot,
        slot,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert slot == correspondence.get_slot_argument()


@pytest.mark.skip
def test_get_non_slot_argument_returns_non_slot():
    location = Mock()
    slot = Slot(Mock(), Mock(), Mock(), locations=[location])
    non_slot = Mock()
    correspondence = Correspondence(
        Mock(),
        Mock(),
        slot,
        non_slot,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert non_slot == correspondence.get_non_slot_argument()
    correspondence = Correspondence(
        Mock(),
        Mock(),
        non_slot,
        slot,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert non_slot == correspondence.get_non_slot_argument()


def test_common_arguments_with():
    arg_1 = Mock()
    arg_2 = Mock()
    arg_3 = Mock()
    arg_4 = Mock()
    correspondence_1 = Correspondence(
        Mock(),
        Mock(),
        arg_1,
        arg_2,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    correspondence_2 = Correspondence(
        Mock(),
        Mock(),
        arg_1,
        arg_2,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    correspondence_3 = Correspondence(
        Mock(),
        Mock(),
        arg_1,
        arg_3,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    correspondence_4 = Correspondence(
        Mock(),
        Mock(),
        arg_2,
        arg_3,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    correspondence_5 = Correspondence(
        Mock(),
        Mock(),
        arg_3,
        arg_4,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert 2 == len(correspondence_1.common_arguments_with(correspondence_2))
    assert 1 == len(correspondence_1.common_arguments_with(correspondence_3))
    assert 1 == len(correspondence_1.common_arguments_with(correspondence_4))
    assert 0 == len(correspondence_1.common_arguments_with(correspondence_5))
