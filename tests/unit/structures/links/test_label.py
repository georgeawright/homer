import pytest
from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.links import Label


def test_copy(bubble_chamber):
    old_start = Mock()
    new_start = Mock()
    parent_id = "id"
    location_1 = Mock()
    location_1.space.name = ""
    location_2 = Mock()
    location_2.space.name = ""
    label = Label(
        Mock(),
        Mock(),
        old_start,
        bubble_chamber.new_structure_collection(old_start),
        Mock(),
        [location_1, location_2],
        Mock(),
        location_1.space,
        Mock(),
        Mock(),
        Mock(),
    )
    copy = label.copy(
        start=new_start, parent_id=parent_id, bubble_chamber=bubble_chamber
    )
    assert label.start == old_start
    assert copy.start == new_start
    assert copy.parent_id == parent_id


def test_nearby(bubble_chamber):
    parent_spaces = Mock()
    start = Mock()
    location_1 = Mock()
    location_1.space.name = ""
    location_2 = Mock()
    location_2.space.name = ""
    label = Label(
        Mock(),
        Mock(),
        start,
        Mock(),
        Mock(),
        [location_1, location_2],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        parent_spaces,
    )
    nearby_label = Mock()
    nearby_label.parent_spaces = parent_spaces
    not_nearby_label = Mock()
    start.labels = bubble_chamber.new_structure_collection(
        label, nearby_label, not_nearby_label
    )
    assert 1 == len(label.nearby())
    assert nearby_label in label.nearby()
    assert not_nearby_label not in label.nearby()
