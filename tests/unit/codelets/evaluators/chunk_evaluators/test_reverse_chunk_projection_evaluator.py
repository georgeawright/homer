import pytest
from unittest.mock import Mock

from homer.codelets.evaluators.chunk_evaluators import ReverseChunkProjectionEvaluator
from homer.codelets.selectors.chunk_selectors import ReverseChunkProjectionSelector
from homer.structure_collection import StructureCollection


@pytest.mark.skip
@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(current_quality, classification):
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "chunk": Mock()}
    label = Mock()
    label.parent_concept.classifier.classify.return_value = classification
    relation = Mock()
    relation.parent_concept.classifier.classify.return_value = classification
    parent_chunk = Mock()
    parent_chunk.labels = StructureCollection({label})
    parent_chunk.relations = StructureCollection({relation})
    chunk = Mock()
    chunk.is_chunk = True
    chunk.members = StructureCollection()
    chunk.quality = current_quality
    chunk.chunks_made_from_this_chunk = StructureCollection({parent_chunk})
    correspondence = Mock()
    correspondence.quality = current_quality
    evaluator = ReverseChunkProjectionEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({chunk, correspondence}),
        Mock(),
    )
    evaluator.run()
    assert classification == chunk.quality
    assert classification == correspondence.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ReverseChunkProjectionSelector)
