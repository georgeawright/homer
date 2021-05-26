import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.suggesters import ChunkSuggester
from homer.codelets.builders import ChunkBuilder
from homer.structure_collection import StructureCollection
from homer.structures.links import Label
from homer.structures.nodes import Chunk
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"chunk": Mock(), "suggest": Mock()}
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
    chunk.value = [[20]]
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
    chunk.value = [[20]]
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


def test_gives_high_confidence_to_compatible_chunks(bubble_chamber, target_chunk):
    target_structures = {"target_one": target_chunk}
    chunk_suggester = ChunkSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    result = chunk_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert chunk_suggester.confidence == 1
    assert len(chunk_suggester.child_codelets) == 1
    assert isinstance(chunk_suggester.child_codelets[0], ChunkBuilder)


def test_gives_low_confidence_incompatible_chunks(
    bubble_chamber, target_chunk, common_space
):
    common_space.proximity_between.return_value = 0.0
    target_structures = {"target_one": target_chunk}
    chunk_suggester = ChunkSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1.0
    )
    result = chunk_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert chunk_suggester.confidence == 0
    assert len(chunk_suggester.child_codelets) == 1
    assert isinstance(chunk_suggester.child_codelets[0], ChunkBuilder)


def test_fizzles_when_no_second_target(bubble_chamber, target_chunk):
    target_chunk.nearby.return_value = StructureCollection()
    urgency = 1.0
    target_structures = {"target_one": target_chunk}
    chunk_suggester = ChunkSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, urgency
    )
    result = chunk_suggester.run()
    assert CodeletResult.FIZZLE == result


def test_fizzles_when_chunk_already_exists(bubble_chamber, target_chunk):
    bubble_chamber.has_chunk.return_value = True
    urgency = 1.0
    target_structures = {"target_one": target_chunk}
    chunk_suggester = ChunkSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, urgency
    )
    result = chunk_suggester.run()
    assert CodeletResult.FIZZLE == result
