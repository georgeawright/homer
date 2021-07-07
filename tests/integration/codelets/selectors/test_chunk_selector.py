import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors import ChunkSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import WorkingSpace
from homer.tools import centroid_euclidean_distance


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    chunk_concept = Concept(
        Mock(),
        Mock(),
        "chunk",
        Mock(),
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(chunk_concept)
    select_concept = Concept(
        Mock(),
        Mock(),
        "select",
        Mock(),
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(select_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, select_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    select_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def target_space():
    parent_concept = Concept(
        "",
        "",
        "",
        [],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
        distance_to_proximity_weight=1.5,
    )
    space = WorkingSpace(
        Mock(),
        Mock(),
        Mock(),
        parent_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def chunk_members():
    member_1 = Mock()
    member_1.size = 1
    member_2 = Mock()
    member_2.size = 1
    members = StructureCollection({member_1, member_2})
    return members


@pytest.fixture
def good_chunk(target_space, chunk_members):
    chunk = Chunk(
        Mock(),
        Mock(),
        [Location([[0, 0]], target_space)],
        chunk_members,
        Mock(),
        1.0,
    )
    chunk._activation = 0.0
    target_space.contents.add(chunk)
    return chunk


@pytest.fixture
def bad_chunk(target_space, chunk_members):
    chunk = Chunk(
        Mock(),
        Mock(),
        [Location([[0, 1]], target_space)],
        chunk_members,
        Mock(),
        0.0,
    )
    chunk._activation = 1.0
    target_space.contents.add(chunk)
    return chunk


def test_good_chunk_is_boosted_bad_chunk_is_decayed(
    bubble_chamber, good_chunk, bad_chunk
):
    original_good_chunk_activation = good_chunk.activation
    original_bad_chunk_activation = bad_chunk.activation
    parent_id = ""
    champion = bad_chunk
    urgency = 1.0
    selector = ChunkSelector.spawn(
        parent_id, bubble_chamber, StructureCollection({champion}), urgency
    )
    selector.run()
    good_chunk.update_activation()
    bad_chunk.update_activation()
    assert good_chunk.activation > original_good_chunk_activation
    assert bad_chunk.activation < original_bad_chunk_activation
