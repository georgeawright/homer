import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.chunk_builders import ReverseChunkProjectionBuilder
from homer.codelets.suggesters.chunk_suggesters import ReverseChunkProjectionSuggester
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Chunk
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"suggest": Mock(), "chunk": Mock(), "same": Mock()}
    return chamber


@pytest.fixture
def target_view(bubble_chamber):
    view = Mock()
    existing_chunk = Mock()
    existing_chunk.members = StructureCollection()
    view.interpretation_space.contents.of_type.return_value = StructureCollection(
        {existing_chunk}
    )
    bubble_chamber.monitoring_views.get_active.return_value = view
    return view


@pytest.fixture
def temperature_interpretation_space():
    space = Mock()
    return space


@pytest.fixture
def target_interpretation_chunk(temperature_interpretation_space):
    chunk = Mock()
    chunk.members = StructureCollection()
    chunk.parent_spaces = StructureCollection({temperature_interpretation_space})
    link = Mock()
    link.parent_concept.classifier.classify.return_value = 1
    chunk.links = StructureCollection({link})
    chunk.correspondences = StructureCollection()
    chunk.labels = StructureCollection({link})
    chunk.links_out = StructureCollection()
    chunk.links_in = StructureCollection()
    return chunk


@pytest.fixture
def target_raw_chunk():
    chunk = Mock()
    chunk.has_correspondence_to_space.return_value = False
    chunk.value = [[10]]
    location = Mock()
    location.coordinates = [[0, 0]]
    chunk.location_in_conceptual_space.return_value = location
    return chunk


def test_gives_high_confidence_for_compatible_chunk(
    bubble_chamber, target_view, target_interpretation_chunk, target_raw_chunk
):
    target_structures = {
        "target_view": target_view,
        "target_interpretation_chunk": target_interpretation_chunk,
        "target_raw_chunk": target_raw_chunk,
    }
    suggester = ReverseChunkProjectionSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        1,
    )
    result = suggester.run()
    assert CodeletResult.SUCCESS == result
    assert suggester.confidence == 1
    assert len(suggester.child_codelets) == 1
    assert isinstance(suggester.child_codelets[0], ReverseChunkProjectionBuilder)


def test_gives_low_confidence_for_incompatible_chunk(
    bubble_chamber, target_view, target_interpretation_chunk, target_raw_chunk
):
    link_1 = Mock()
    link_1.parent_concept.classifier.classify.return_value = 0
    link_2 = Mock()
    link_2.parent_concept.classifier.classify.return_value = 0
    target_interpretation_chunk.links = StructureCollection({link_1, link_2})
    target_structures = {
        "target_view": target_view,
        "target_interpretation_chunk": target_interpretation_chunk,
        "target_raw_chunk": target_raw_chunk,
    }
    suggester = ReverseChunkProjectionSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        1.0,
    )
    result = suggester.run()
    assert CodeletResult.SUCCESS == result
    assert suggester.confidence == 0
    assert len(suggester.child_codelets) == 1
    assert isinstance(suggester.child_codelets[0], ReverseChunkProjectionBuilder)


def test_fizzles_when_raw_chunk_has_correspondence_to_interpretation_space(
    bubble_chamber, target_view, target_interpretation_chunk, target_raw_chunk
):
    target_raw_chunk.has_correspondence_to_space.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_interpretation_chunk": target_interpretation_chunk,
        "target_raw_chunk": target_raw_chunk,
    }
    urgency = 1.0
    suggester = ReverseChunkProjectionSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        urgency,
    )
    result = suggester.run()
    assert CodeletResult.FIZZLE == result
