import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.chunk_evaluators import ChunkProjectionEvaluator
from homer.codelets.selectors.chunk_selectors import ChunkProjectionSelector
from homer.structure_collection import StructureCollection


@pytest.mark.skip
@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "chunk": Mock()}
    chunk_member_1 = Mock()
    chunk_member_1.quality = classification
    chunk_member_2 = Mock()
    chunk_member_2.quality = classification
    chunk = Mock()
    chunk.is_chunk = True
    chunk.members = StructureCollection({chunk_member_1, chunk_member_2})
    chunk.quality = current_quality
    evaluator = ChunkProjectionEvaluator(
        Mock(), Mock(), bubble_chamber, StructureCollection({chunk}), Mock()
    )
    evaluator.run()
    assert classification == chunk.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ChunkProjectionSelector)
