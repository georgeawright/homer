import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder
from homer.codelets.evaluators import ChunkEvaluator
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
    build_concept = Concept(
        Mock(),
        Mock(),
        "build",
        Mock(),
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, build_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def target_chunk(bubble_chamber):
    location_concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        "coordinates",
        Mock(),
        math.dist,
    )
    input_space = WorkingSpace(
        Mock(),
        Mock(),
        "input",
        location_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
        is_basic_level=True,
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        [Location([0, 0], input_space)],
        StructureCollection(),
        Mock(),
        0.0,
    )
    second_chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        [Location([0, 1], input_space)],
        StructureCollection(),
        Mock(),
        0.0,
    )
    bubble_chamber.chunks.add(chunk)
    bubble_chamber.chunks.add(second_chunk)
    input_space.contents.add(chunk)
    input_space.contents.add(second_chunk)
    chunk.parent_spaces.add(input_space)
    return chunk


def test_successful_adds_member_to_chunk_and_spawns_follow_up_and_same_chunk_cannot_be_recreated(
    bubble_chamber, target_chunk
):
    parent_id = ""
    urgency = 1.0

    builder = ChunkBuilder.spawn(parent_id, bubble_chamber, target_chunk, urgency)
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Chunk)
    assert isinstance(builder.child_codelets[0], ChunkEvaluator)
    builder = ChunkBuilder.spawn(parent_id, bubble_chamber, target_chunk, urgency)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
