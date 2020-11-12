from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.chunks import Slot
from homer.structures.links import Correspondence


def test_nearby():
    start = Mock()
    start.correspondences = StructureCollection({Mock()})
    end = Mock()
    end.correspondences = StructureCollection({Mock()})
    parent_space = Mock()
    parent_space.contents = StructureCollection({Mock()})
    correspondence = Correspondence(
        start, end, Mock(), Mock(), Mock(), parent_space, Mock(), Mock()
    )
    parent_space.contents.add(correspondence)
    neighbours = correspondence.nearby()
    assert 3 == len(neighbours)
    assert correspondence not in neighbours


def test_get_slot_argument_returns_slot():
    slot = Slot()
    non_slot = Mock()
    correspondence = Correspondence(
        slot, non_slot, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    assert slot == correspondence.get_slot_argument()
    correspondence = Correspondence(
        non_slot, slot, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    assert slot == correspondence.get_slot_argument()


def test_get_non_slot_argument_returns_non_slot():
    slot = Slot()
    non_slot = Mock()
    correspondence = Correspondence(
        slot, non_slot, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    assert non_slot == correspondence.get_non_slot_argument()
    correspondence = Correspondence(
        non_slot, slot, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    assert non_slot == correspondence.get_non_slot_argument()


def test_common_arguments_with():
    arg_1 = Mock()
    arg_2 = Mock()
    arg_3 = Mock()
    arg_4 = Mock()
    correspondence_1 = Correspondence(
        arg_1, arg_2, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    correspondence_2 = Correspondence(
        arg_1, arg_2, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    correspondence_3 = Correspondence(
        arg_1, arg_3, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    correspondence_4 = Correspondence(
        arg_2, arg_3, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    correspondence_5 = Correspondence(
        arg_3, arg_4, Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    assert 2 == len(correspondence_1.common_arguments_with(correspondence_2))
    assert 1 == len(correspondence_1.common_arguments_with(correspondence_3))
    assert 1 == len(correspondence_1.common_arguments_with(correspondence_4))
    assert 0 == len(correspondence_1.common_arguments_with(correspondence_5))
