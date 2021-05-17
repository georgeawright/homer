import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder
from homer.codelets.evaluators import ChunkEvaluator
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import WorkingSpace
from homer.tools import centroid_euclidean_distance, hasinstance


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
    build_concept = Concept(
        Mock(),
        Mock(),
        "build",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, build_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    text_concept = Mock()
    text_concept.name = "text"
    chamber.concepts.add(text_concept)
    return chamber


@pytest.fixture
def target_chunk(bubble_chamber):
    input_concept = Concept(
        Mock(),
        Mock(),
        "input",
        Mock(),
        Mock(),
        "coordinates",
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    bubble_chamber.concepts.add(input_concept)
    input_space = WorkingSpace(
        Mock(),
        Mock(),
        "input",
        input_concept,
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
        [[10]],
        [Location([[0, 0]], input_space)],
        StructureCollection(),
        input_space,
        0.0,
    )
    second_chunk = Chunk(
        Mock(),
        Mock(),
        [[10]],
        [Location([[0, 1]], input_space)],
        StructureCollection(),
        input_space,
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
    assert hasinstance(builder.child_structures, Chunk)
    assert isinstance(builder.child_codelets[0], ChunkEvaluator)
    builder = ChunkBuilder.spawn(parent_id, bubble_chamber, target_chunk, urgency)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
