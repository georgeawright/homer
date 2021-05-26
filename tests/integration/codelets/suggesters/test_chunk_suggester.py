import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder
from homer.codelets.suggesters import ChunkSuggester
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import WorkingSpace
from homer.tools import centroid_euclidean_distance, hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
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
    suggest_concept = Concept(
        Mock(),
        Mock(),
        "suggest",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(suggest_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, suggest_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    suggest_concept.links_in.add(relation)
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


def test_gives_high_confidence_for_compatible_chunks_and_spawns_follow_up(
    bubble_chamber, target_chunk
):
    parent_id = ""
    urgency = 1.0
    suggester = ChunkSuggester.spawn(
        parent_id,
        bubble_chamber,
        {"target_one": target_chunk, "target_two": None},
        urgency,
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert isinstance(suggester.child_codelets[0], ChunkBuilder)
