import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators.chunk_evaluators import ChunkProjectionEvaluator
from homer.codelets.selectors.chunk_selectors import ChunkProjectionSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import WorkingSpace


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    chunk_concept = Concept(
        Mock(),
        Mock(),
        "chunk",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(chunk_concept)
    evaluate_concept = Concept(
        Mock(),
        Mock(),
        "evaluate",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(evaluate_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, evaluate_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    evaluate_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def good_chunk(bubble_chamber):
    member_1 = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection(),
        Mock(),
        1.0,
    )
    member_2 = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection(),
        Mock(),
        1.0,
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({member_1, member_2}),
        Mock(),
        0.0,
    )
    bubble_chamber.chunks.add(chunk)
    return chunk


@pytest.fixture
def bad_chunk(bubble_chamber):
    member_1 = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection(),
        Mock(),
        0.0,
    )
    member_2 = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection(),
        Mock(),
        0.0,
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        StructureCollection({member_1, member_2}),
        Mock(),
        1.0,
    )
    bubble_chamber.chunks.add(chunk)
    return chunk


def test_increases_quality_of_good_chunk(bubble_chamber, good_chunk):
    original_chunk_quality = good_chunk.quality
    parent_id = ""
    urgency = 1.0
    evaluator = ChunkProjectionEvaluator.spawn(
        parent_id, bubble_chamber, StructureCollection({good_chunk}), urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_chunk.quality > original_chunk_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ChunkProjectionSelector)


def test_decreases_quality_of_bad_chunk(bubble_chamber, bad_chunk):
    original_chunk_quality = bad_chunk.quality
    parent_id = ""
    urgency = 1.0
    evaluator = ChunkProjectionEvaluator.spawn(
        parent_id, bubble_chamber, StructureCollection({bad_chunk}), urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_chunk.quality < original_chunk_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ChunkProjectionSelector)
