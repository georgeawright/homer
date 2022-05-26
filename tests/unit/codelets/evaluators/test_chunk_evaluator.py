import pytest
from unittest.mock import Mock, patch

from linguoplotter.classifiers import SamenessClassifier
from linguoplotter.codelets.evaluators import ChunkEvaluator
from linguoplotter.codelets.selectors import ChunkSelector
from linguoplotter.structure_collection import StructureCollection


@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(
    bubble_chamber, current_quality, classification
):
    with patch.object(SamenessClassifier, "classify", return_value=classification):
        chunk = Mock()
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
