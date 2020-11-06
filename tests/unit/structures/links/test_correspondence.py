from unittest.mock import Mock

from homer.structures.chunks import Slot
from homer.structures.links import Correspondence


def test_get_slot_argument_returns_slot():
    slot = Slot()
    non_slot = Mock()
    correspondence = Correspondence(slot, non_slot, Mock(), Mock())
    assert slot == correspondence.get_slot_argument()
    correspondence = Correspondence(non_slot, slot, Mock(), Mock())
    assert slot == correspondence.get_slot_argument()


def test_get_non_slot_argument_returns_non_slot():
    slot = Slot()
    non_slot = Mock()
    correspondence = Correspondence(slot, non_slot, Mock(), Mock())
    assert non_slot == correspondence.get_non_slot_argument()
    correspondence = Correspondence(non_slot, slot, Mock(), Mock())
    assert non_slot == correspondence.get_non_slot_argument()
