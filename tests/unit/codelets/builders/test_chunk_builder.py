import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder
from homer.codelets.evaluators import ChunkEvaluator
from homer.structure_collection import StructureCollection
from homer.structures import Chunk
from homer.structures.links import Label


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"chunk": Mock(), "build": Mock()}
    chamber.has_chunk.return_value = False
    chamber.chunks.get_unhappy.return_value = Mock()
    return chamber


@pytest.fixture
def common_space():
    space = Mock()
    space.is_sub_space = False
    space.proximity_between.return_value = 1.0
    space.parent_concept.relevant_value = "value"
    return space


@pytest.fixture
def second_target_chunk(common_space):
    location = Mock()
    location.coordinates = [1, 1]
    location.space = common_space
    chunk = Mock()
    chunk.value = [20]
    chunk.size = 1
    chunk.activation = 0.5
    chunk.quality = 0.5
    chunk.location_in_space.return_value = location
    chunk.neighbours = StructureCollection()
    chunk.parent_spaces = StructureCollection({common_space})
    chunk.links_in = StructureCollection()
    chunk.links_out = StructureCollection()
    chunk.labels = []
    chunk.relations = []
    chunk.correspondences = []
    return chunk


@pytest.fixture
def target_chunk(common_space, second_target_chunk):
    location = Mock()
    location.coordinates = [2, 2]
    location.space = common_space
    chunk = Mock()
    chunk.value = [20]
    chunk.size = 1
    chunk.activation = 0.5
    chunk.quality = 0.5
    chunk.location_in_space.return_value = location
    chunk.members = StructureCollection()
    chunk.neighbours = StructureCollection()
    chunk.parent_spaces = StructureCollection({common_space})
    chunk.nearby.return_value = StructureCollection({second_target_chunk})
    chunk.links_in = StructureCollection()
    chunk.links_out = StructureCollection()
    chunk.labels = []
    chunk.relations = []
    chunk.correspondences = []
    return chunk


def test_successful_creates_chunk_and_spawns_follow_up(bubble_chamber, target_chunk):
    chunk_builder = ChunkBuilder(Mock(), Mock(), bubble_chamber, target_chunk, Mock())
    result = chunk_builder.run()
    assert CodeletResult.SUCCESS == result
    assert isinstance(chunk_builder.child_structure, Chunk)
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkEvaluator)


def test_new_chunk_has_no_duplicate_links(
    bubble_chamber, target_chunk, second_target_chunk, common_space
):
    concept = Mock()
    label_1 = Label(Mock(), Mock(), target_chunk, concept, common_space, Mock())
    label_2 = Label(Mock(), Mock(), second_target_chunk, concept, common_space, Mock())
    target_chunk.links_out.add(label_1)
    second_target_chunk.links_out.add(label_2)
    chunk_builder = ChunkBuilder(Mock(), Mock(), bubble_chamber, target_chunk, Mock())
    result = chunk_builder.run()
    assert CodeletResult.SUCCESS == result
    assert len(chunk_builder.child_structure.links) == 1


def test_fails_when_chunks_are_incompatible(bubble_chamber, target_chunk, common_space):
    common_space.proximity_between.return_value = 0.0
    chunk_builder = ChunkBuilder(Mock(), Mock(), bubble_chamber, target_chunk, Mock())
    result = chunk_builder.run()
    assert CodeletResult.FAIL == result
    assert chunk_builder.child_structure is None
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkBuilder)


def test_fizzles_when_no_second_target(bubble_chamber, target_chunk):
    target_chunk.nearby.return_value = StructureCollection()
    urgency = 1.0
    chunk_builder = ChunkBuilder(Mock(), Mock(), bubble_chamber, target_chunk, urgency)
    result = chunk_builder.run()
    assert CodeletResult.FIZZLE == result
    assert chunk_builder.child_structure is None
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkBuilder)


def test_fizzles_when_chunk_already_exists(bubble_chamber, target_chunk):
    bubble_chamber.has_chunk.return_value = True
    urgency = 1.0
    chunk_builder = ChunkBuilder(Mock(), Mock(), bubble_chamber, target_chunk, urgency)
    result = chunk_builder.run()
    assert CodeletResult.FIZZLE == result
    assert chunk_builder.child_structure is None
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkBuilder)
