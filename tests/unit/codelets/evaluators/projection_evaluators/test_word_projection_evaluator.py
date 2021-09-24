import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.projection_evaluators import WordProjectionEvaluator
from homer.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, label_quality", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, label_quality):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "word": Mock()}

    label = Mock()
    label.is_slot = False
    label.quality = label_quality

    correspondence_to_frame = Mock()
    correspondence_to_frame.quality = 1.0
    label.correspondences_with.return_value = StructureCollection(
        {correspondence_to_frame}
    )

    slot = Mock()
    slot.is_slot = True

    word = Mock()
    word.is_word = True
    word.quality = current_quality

    label_to_word_correspondence = Mock()
    label_to_word_correspondence.is_correspondence = True
    label_to_word_correspondence.start = label
    label_to_word_correspondence.quality = current_quality
    slot_to_word_correspondence = Mock()
    slot_to_word_correspondence.is_correspondence = True
    slot_to_word_correspondence.start = slot
    slot_to_word_correspondence.quality = current_quality
    word.correspondences = StructureCollection(
        {label_to_word_correspondence, slot_to_word_correspondence}
    )

    evaluator = WordProjectionEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection(
            {word, label_to_word_correspondence, slot_to_word_correspondence}
        ),
        Mock(),
    )
    evaluator.run()
    assert word.quality == label_quality


def test_gives_function_word_maximum_quality():
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "word": Mock()}
    word = Mock()
    word.is_word = True
    word.quality = 0
    correspondee = Mock()
    correspondee.labels = StructureCollection()
    word.correspondees = StructureCollection({correspondee})
    evaluator = WordProjectionEvaluator(
        Mock(), Mock(), bubble_chamber, StructureCollection({word}), Mock()
    )
    evaluator.run()
    assert 1 == word.quality
