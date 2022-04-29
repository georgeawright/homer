import pytest
from unittest.mock import Mock

from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Label


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
