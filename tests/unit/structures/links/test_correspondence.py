from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.chunks import Slot
from homer.structures.links import Correspondence


def test_copy():
    old_start = Mock()
    old_end = Mock()
    new_start = Mock()
    new_end = Mock()
    parent_id = "id"
    correspondence = Correspondence(
        Mock(),
        Mock(),
        old_start,
        old_end,
        Mock(),
        Mock(),
        Mock(),
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
    correspondence = Correspondence(
        Mock(), Mock(), start, end, Mock(), Mock(), Mock(), parent_space, Mock(), Mock()
    )
    parent_space.contents.add(correspondence)
    neighbours = correspondence.nearby()
    assert 3 == len(neighbours)
    assert correspondence not in neighbours


def test_get_slot_argument_returns_slot():
    slot = Slot(Mock(), Mock())
    non_slot = Mock()
    correspondence = Correspondence(
        Mock(), Mock(), slot, non_slot, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    assert slot == correspondence.get_slot_argument()
    correspondence = Correspondence(
        Mock(), Mock(), non_slot, slot, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    assert slot == correspondence.get_slot_argument()


def test_get_non_slot_argument_returns_non_slot():
    slot = Slot(Mock(), Mock())
    non_slot = Mock()
    correspondence = Correspondence(
        Mock(), Mock(), slot, non_slot, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    assert non_slot == correspondence.get_non_slot_argument()
    correspondence = Correspondence(
        Mock(), Mock(), non_slot, slot, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    assert non_slot == correspondence.get_non_slot_argument()


def test_common_arguments_with():
    arg_1 = Mock()
    arg_2 = Mock()
    arg_3 = Mock()
    arg_4 = Mock()
    correspondence_1 = Correspondence(
        Mock(), Mock(), arg_1, arg_2, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    correspondence_2 = Correspondence(
        Mock(), Mock(), arg_1, arg_2, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    correspondence_3 = Correspondence(
        Mock(), Mock(), arg_1, arg_3, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    correspondence_4 = Correspondence(
        Mock(), Mock(), arg_2, arg_3, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    correspondence_5 = Correspondence(
        Mock(), Mock(), arg_3, arg_4, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    assert 2 == len(correspondence_1.common_arguments_with(correspondence_2))
    assert 1 == len(correspondence_1.common_arguments_with(correspondence_3))
    assert 1 == len(correspondence_1.common_arguments_with(correspondence_4))
    assert 0 == len(correspondence_1.common_arguments_with(correspondence_5))
