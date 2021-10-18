import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.selectors.projection_selectors import LabelProjectionSelector
from homer.structure_collection import StructureCollection


def test_label_is_boosted(bubble_chamber):
    label = Mock()
    label.size = 1
    label.quality = 1.0
    label.activation = 0.0

    parent_concept = Mock()
    correspondence_from_frame = Mock()
    correspondence_from_frame.is_correspondence = True
    correspondence_from_frame.start.parent_space.is_frame = True
    correspondence_from_frame.start.parent_space.parent_concept = parent_concept
    correspondence_from_frame.end.parent_space.parent_concept = parent_concept
    correspondence_from_frame.quality = 1.0
    correspondence_from_frame.activation = 1.0

    selector = LabelProjectionSelector(
        Mock(),
        Mock(),
        bubble_chamber,
        bubble_chamber.new_structure_collection(label, correspondence_from_frame),
        Mock(),
    )
    selector.run()
    assert CodeletResult.SUCCESS == selector.result
    assert label.boost_activation.is_called()
