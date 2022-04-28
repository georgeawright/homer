import pytest
from unittest.mock import Mock

from linguoplotter.codelets.evaluators.projection_evaluators import (
    LetterChunkProjectionEvaluator,
)
from linguoplotter.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, label_quality", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(
    bubble_chamber, current_quality, label_quality
):
    label = Mock()
    label.is_slot = False
    label.quality = label_quality

    correspondence_to_frame = Mock()
    correspondence_to_frame.quality = 1.0
    label.correspondences_with.return_value = bubble_chamber.new_structure_collection(
        correspondence_to_frame
    )

    slot = Mock()
    slot.is_slot = True

    word = Mock()
    word.is_letter_chunk = True
    word.quality = current_quality

    label_to_word_correspondence = Mock()
    label_to_word_correspondence.is_correspondence = True
    label_to_word_correspondence.start = label
    label_to_word_correspondence.quality = current_quality
    slot_to_word_correspondence = Mock()
    slot_to_word_correspondence.is_correspondence = True
    slot_to_word_correspondence.start = slot
    slot_to_word_correspondence.quality = current_quality
    word.correspondences = bubble_chamber.new_structure_collection(
        label_to_word_correspondence, slot_to_word_correspondence
    )

    evaluator = LetterChunkProjectionEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        bubble_chamber.new_structure_collection(
            word, label_to_word_correspondence, slot_to_word_correspondence
        ),
        Mock(),
    )
    evaluator.run()
    assert word.quality == label_quality


def test_gives_function_word_maximum_quality(bubble_chamber):
    word = Mock()
    word.is_letter_chunk = True
    word.quality = 0
    correspondee = Mock()
    correspondee.labels = bubble_chamber.new_structure_collection()
    word.correspondees = bubble_chamber.new_structure_collection(correspondee)
    evaluator = LetterChunkProjectionEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        bubble_chamber.new_structure_collection(word),
        Mock(),
    )
    evaluator.run()
    assert 1 == word.quality
