import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.projection_evaluators import RelationProjectionEvaluator
from homer.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, word_quality", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, word_quality):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "relation": Mock()}

    word = Mock()
    word.is_slot = False
    word.quality = word_quality

    correspondence_to_frame = Mock()
    correspondence_to_frame.quality = 1.0
    word.correspondences_with.return_value = StructureCollection(
        {correspondence_to_frame}
    )

    slot = Mock()
    slot.is_slot = True

    relation = Mock()
    relation.is_relation = True
    relation.quality = current_quality

    word_to_relation_correspondence = Mock()
    word_to_relation_correspondence.is_correspondence = True
    word_to_relation_correspondence.start = word
    word_to_relation_correspondence.quality = current_quality
    slot_to_relation_correspondence = Mock()
    slot_to_relation_correspondence.is_correspondence = True
    slot_to_relation_correspondence.start = slot
    slot_to_relation_correspondence.quality = current_quality
    word.correspondences = StructureCollection(
        {word_to_relation_correspondence, slot_to_relation_correspondence}
    )

    evaluator = RelationProjectionEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection(
            {relation, word_to_relation_correspondence, slot_to_relation_correspondence}
        ),
        Mock(),
    )
    evaluator.run()
    assert relation.quality == word_quality
