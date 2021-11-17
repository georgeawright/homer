import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.projection_evaluators import LabelProjectionEvaluator
from homer.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, word_quality", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(
    bubble_chamber, current_quality, word_quality
):
    word = Mock()
    word.is_slot = False
    word.quality = word_quality

    correspondence_to_frame = Mock()
    correspondence_to_frame.quality = 1.0
    word.correspondences_with.return_value = bubble_chamber.new_structure_collection(
        correspondence_to_frame
    )

    slot = Mock()
    slot.is_slot = True

    label = Mock()
    label.is_label = True
    label.quality = current_quality

    word_to_label_correspondence = Mock()
    word_to_label_correspondence.is_correspondence = True
    word_to_label_correspondence.start = word
    word_to_label_correspondence.quality = current_quality
    slot_to_label_correspondence = Mock()
    slot_to_label_correspondence.is_correspondence = True
    slot_to_label_correspondence.start = slot
    slot_to_label_correspondence.quality = current_quality
    word.correspondences = bubble_chamber.new_structure_collection(
        word_to_label_correspondence, slot_to_label_correspondence
    )

    evaluator = LabelProjectionEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        bubble_chamber.new_structure_collection(
            label, word_to_label_correspondence, slot_to_label_correspondence
        ),
        Mock(),
    )
    evaluator.run()
    assert label.quality == word_quality
