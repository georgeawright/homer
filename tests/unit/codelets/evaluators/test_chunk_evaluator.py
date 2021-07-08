import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import ChunkEvaluator
from homer.codelets.selectors import ChunkSelector
from homer.structure_collection import StructureCollection


@pytest.mark.skip
@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "chunk": Mock()}
    chunk = Mock()
    chunk.members = StructureCollection({Mock(), Mock()})
    space = Mock()
    space.is_sub_space = False
    space.proximity_between.return_value = classification
    chunk.parent_spaces = StructureCollection({space})
    chunk.quality = current_quality
    evaluator = ChunkEvaluator(
        Mock(), Mock(), bubble_chamber, StructureCollection({chunk}), Mock()
    )
    evaluator.run()
    assert classification == chunk.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ChunkSelector)
