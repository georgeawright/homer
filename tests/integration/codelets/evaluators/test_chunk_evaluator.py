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
        StructureCollection(),
        None,
    )
    chamber.concepts.add(evaluate_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, evaluate_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    evaluate_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def location_concept():
    concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    return concept


@pytest.fixture
def input_space(location_concept):
    space = WorkingSpace(
        Mock(),
        Mock(),
        "input",
        location_concept,
        [],
        StructureCollection(),
        0,
        [],
        [],
        is_basic_level=True,
    )
    return space


@pytest.fixture
def good_chunk(bubble_chamber, location_concept, input_space):
    member_1 = Chunk(
        Mock(),
        Mock(),
        [10],
        [Location([0, 0], input_space)],
        StructureCollection(),
        0.0,
    )
    member_2 = Chunk(
        Mock(),
        Mock(),
        [10],
        [Location([0, 1], input_space)],
        StructureCollection(),
        0.0,
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        [Location([0, 0], input_space)],
        StructureCollection({member_1, member_2}),
        0.0,
    )
    bubble_chamber.chunks.add(chunk)
    input_space.contents.add(chunk)
    return chunk


@pytest.fixture
def bad_chunk(bubble_chamber, location_concept, input_space):
    temperature_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    temperature_space = WorkingSpace(
        Mock(),
        Mock(),
        "temperature",
        temperature_concept,
        [],
        StructureCollection(),
        1,
        [],
        [],
        is_basic_level=True,
    )
    member_1 = Chunk(
        Mock(),
        Mock(),
        [12],
        [Location([0, 0], input_space), Location([12], temperature_space)],
        StructureCollection(),
        0.0,
    )
    member_2 = Chunk(
        Mock(),
        Mock(),
        [5],
        [Location([0, 1], input_space), Location([5], temperature_space)],
        StructureCollection(),
        0.0,
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        [8.5],
        [Location([0, 0], input_space), Location([8.5], temperature_space)],
        StructureCollection({member_1, member_2}),
        1.0,
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
