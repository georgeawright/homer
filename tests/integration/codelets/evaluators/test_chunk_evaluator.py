import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators import ChunkEvaluator
from homer.codelets.selectors import ChunkSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.links import Relation
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
        Mock(),
    )
    chunk_concept = Concept(
        Mock(),
        Mock(),
        "chunk",
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(chunk_concept)
    evaluate_concept = Concept(
        Mock(),
        Mock(),
        "evaluate",
        None,
        None,
        None,
        "value",
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
    location_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    input_space = WorkingSpace(
        Mock(), Mock(), "input", StructureCollection(), 0, location_concept
    )
    parent_spaces = StructureCollection({input_space})
    member_1 = Chunk(
        Mock(),
        Mock(),
        [10],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    member_2 = Chunk(
        Mock(),
        Mock(),
        [10],
        Location([0, 1], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        Location([0, 0], input_space),
        StructureCollection({member_1, member_2}),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    bubble_chamber.chunks.add(chunk)
    input_space.contents.add(chunk)
    return chunk


@pytest.fixture
def bad_chunk(bubble_chamber):
    location_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    temperature_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    input_space = WorkingSpace(
        Mock(), Mock(), "input", StructureCollection(), 0, location_concept
    )
    temperature_space = WorkingSpace(
        Mock(), Mock(), "temperature", StructureCollection(), 0, temperature_concept
    )
    parent_spaces = StructureCollection({input_space, temperature_space})
    member_1 = Chunk(
        Mock(),
        Mock(),
        [12],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    member_2 = Chunk(
        Mock(),
        Mock(),
        [5],
        Location([0, 1], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        [8.5],
        Location([0, 0], input_space),
        StructureCollection({member_1, member_2}),
        StructureCollection(),
        1.0,
        parent_spaces,
    )
    bubble_chamber.chunks.add(chunk)
    input_space.contents.add(chunk)
    temperature_space.contents.add(chunk)
    return chunk


def test_increases_quality_of_good_chunk(bubble_chamber, good_chunk):
    original_chunk_quality = good_chunk.quality
    parent_id = ""
    urgency = 1.0
    evaluator = ChunkEvaluator.spawn(parent_id, bubble_chamber, good_chunk, urgency)
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_chunk.quality > original_chunk_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ChunkSelector)


def test_decreases_quality_of_bad_chunk(bubble_chamber, bad_chunk):
    original_chunk_quality = bad_chunk.quality
    parent_id = ""
    urgency = 1.0
    evaluator = ChunkEvaluator.spawn(parent_id, bubble_chamber, bad_chunk, urgency)
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_chunk.quality < original_chunk_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], ChunkSelector)
