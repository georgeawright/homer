import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder
from homer.codelets.evaluators import ChunkEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.links import Label
from homer.structures.nodes import Chunk
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"chunk": Mock(), "build": Mock()}
    chamber.has_chunk.return_value = False
    input_space = Mock()
    chunk = Mock()
    chunk.is_chunk = True
    input_space.contents = StructureCollection({chunk})
    chamber.spaces = {"input": input_space}
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
    location.coordinates = [[1, 1]]
    location.space = common_space
    chunk = Mock()
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
    location.coordinates = [[2, 2]]
    location.space = common_space
    chunk = Mock()
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


def test_successful_creates_chunk_and_spawns_follow_up(
    bubble_chamber, target_chunk, second_target_chunk
):
    target_structures = {"target_one": target_chunk, "target_two": second_target_chunk}
    chunk_builder = ChunkBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    result = chunk_builder.run()
    assert CodeletResult.SUCCESS == result
    assert hasinstance(chunk_builder.child_structures, Chunk)
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ChunkEvaluator)


def test_new_chunk_has_no_duplicate_links(
    bubble_chamber, target_chunk, second_target_chunk, common_space
):
    target_structures = {"target_one": target_chunk, "target_two": second_target_chunk}
    concept = Mock()
    label_1 = Label(Mock(), Mock(), target_chunk, concept, common_space, 1)
    label_2 = Label(Mock(), Mock(), second_target_chunk, concept, common_space, 1)
    target_chunk.labels = StructureCollection({label_1})
    second_target_chunk.labels = StructureCollection({label_2})
    chunk_builder = ChunkBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    result = chunk_builder.run()
    assert CodeletResult.SUCCESS == result
    child_structure = chunk_builder.child_structures.get_random()
    assert len(child_structure.links) == 1


def test_fizzles_when_chunk_already_exists(
    bubble_chamber, target_chunk, second_target_chunk
):
    bubble_chamber.has_chunk.return_value = True
    target_structures = {"target_one": target_chunk, "target_two": second_target_chunk}
    urgency = 1.0
    chunk_builder = ChunkBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, urgency
    )
    result = chunk_builder.run()
    assert CodeletResult.FIZZLE == result
    assert chunk_builder.child_structures is None
