from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures import View


def test_copy():
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"text": Mock()}
    bubble_chamber.spaces = {"text": Mock(), "top level working": Mock()}
    word = Mock()
    correspondence_1 = Mock()
    correspondence_2 = Mock()
    correspondence_3 = Mock()
    correspondence_3.end = word
    word.correspondences = StructureCollection({correspondence_3})
    output_space = Mock()
    output_space.contents = StructureCollection({word})
    original_view = View(
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({correspondence_1, correspondence_2, correspondence_3}),
        Mock(),
        output_space,
        Mock(),
    )
    view_copy = original_view.copy(bubble_chamber, Mock(), Mock(), Mock())
    assert isinstance(view_copy, View)
    assert 3 == len(view_copy.members)
    assert 1 == len(view_copy.output_space.contents)
