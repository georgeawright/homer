from unittest.mock import Mock

from homer.codelets.evaluators.projection_evaluators import ChunkProjectionEvaluator
from homer.structure_collection import StructureCollection


def test_gives_chunk_maximum_quality():
    bubble_chamber = Mock()
    bubble_chamber.concepts = {"evaluate": Mock(), "chunk": Mock()}
    chunk = Mock()
    chunk.quality = 0
    evaluator = ChunkProjectionEvaluator(
        Mock(), Mock(), bubble_chamber, StructureCollection({chunk}), Mock()
    )
    evaluator.run()
    assert 1 == chunk.quality
