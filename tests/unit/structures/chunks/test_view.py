from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.chunks import View


def test_copy():
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"text": Mock()}
    bubble_chamber.spaces = {"text": Mock(), "top level working": Mock()}
    correspondence_1 = Mock()
    correspondence_2 = Mock()
    original_view = View(
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({correspondence_1, correspondence_2}),
        Mock(),
        Mock(),
        Mock(),
    )
    view_copy = original_view.copy(bubble_chamber, Mock(), Mock(), Mock())
    assert isinstance(view_copy, View)
