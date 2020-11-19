import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder, ChunkEnlarger
from homer.codelets.selectors import ChunkSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk
from homer.structures.spaces import WorkingSpace


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    return chamber


@pytest.fixture
def target_space():
    space = WorkingSpace(Mock(), StructureCollection(), Mock(), Mock(), Mock(), Mock())
    return space


@pytest.fixture
def chunk_members():
    members = StructureCollection({Mock(), Mock()})
    return members


@pytest.fixture
def good_chunk(target_space, chunk_members):
    chunk = Chunk(
        Mock(),
        Location([0, 0], target_space),
        chunk_members,
        Mock(),
        1.0,
        StructureCollection({target_space}),
    )
    target_space.contents.add(chunk)
    return chunk


@pytest.fixture
def bad_chunk(target_space, chunk_members):
    chunk = Chunk(
        Mock(),
        Location([0, 1], target_space),
        chunk_members,
        Mock(),
        0.0,
        StructureCollection({target_space}),
    )
    target_space.contents.add(chunk)
    return chunk


def test_good_chunk_is_boosted_bad_chunk_is_decayed(
    bubble_chamber, target_space, good_chunk, bad_chunk
):
    parent_id = ""
    champion = bad_chunk
    urgency = 1.0
    selector = ChunkSelector.spawn(
        parent_id, bubble_chamber, target_space, champion, urgency
    )
    for _ in range(20):
        selector.run()
        selector = selector.child_codelets[0]
        good_chunk.update_activation()
        bad_chunk.update_activation()
    assert 1 == good_chunk.activation
    assert 0 == bad_chunk.activation
