import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import ChunkEvaluator
from homer.codelets.selectors import ChunkSelector
from homer.structure_collection import StructureCollection


@pytest.mark.skip
@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(
    bubble_chamber, current_quality, classification
):
    chunk = Mock()
    chunk.is_slot = False
    chunk.rule.right_concept = None
    chunk.rule.left_concept.classifier.classify_chunk.return_value = classification
    chunk.quality = current_quality
    evaluator = ChunkEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        bubble_chamber.new_structure_collection(chunk),
        Mock(),
    )
    evaluator.run()
    assert classification == chunk.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ChunkSelector)
