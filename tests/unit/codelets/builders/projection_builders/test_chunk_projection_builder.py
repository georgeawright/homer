import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.projection_builders import ChunkProjectionBuilder
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence
from homer.structures.nodes import Word
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"build": Mock(), "same": Mock(), "chunk": Mock()}
    chamber.conceptual_spaces = {"grammar": Mock()}
    chamber.chunks = StructureCollection()
    return chamber


@pytest.fixture
def target_view():
    view = Mock()
    view.slot_values = {}
    return view


@pytest.fixture
def target_projectee(target_view):
    chunk = Mock()
    chunk_copy = Mock()
    chunk_copy.locations = []
    chunk.copy_to_location.return_value = chunk_copy
    return chunk


@pytest.fixture
def frame_correspondee(target_projectee, target_view):
    correspondee = Mock()
    correspondee.structure_id = "frame_correspondee"
    frame_correspondence = Mock()
    frame_correspondence.start = correspondee
    frame_correspondence.end = target_projectee
    target_projectee.correspondences = StructureCollection({frame_correspondence})
    non_frame_correspondee = Mock()
    non_frame_correspondence = Mock()
    non_frame_correspondence.start = non_frame_correspondee
    non_frame_correspondence.end = correspondee
    correspondee.correspondences = StructureCollection(
        {non_frame_correspondence, frame_correspondence}
    )
    target_view.members = StructureCollection(
        {frame_correspondence, non_frame_correspondence}
    )
    target_view.slot_values[correspondee.structure_id] = Mock()
    return correspondee


def test_projects_slot_into_output_space(
    bubble_chamber, target_view, target_projectee, frame_correspondee
):
    target_projectee.is_slot = True
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
        "target_correspondence": Mock(),
        "frame_correspondee": frame_correspondee,
        "non_frame": Mock(),
        "non_frame_correspondee": Mock(),
    }
    builder = ChunkProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
    builder.run()
    assert CodeletResult.SUCCESS == builder.result


def test_fizzles_if_chunk_projection_exists(
    bubble_chamber, target_view, target_projectee, frame_correspondee
):
    target_projectee.is_slot = True
    target_view.slot_values[target_projectee.structure_id] = Mock()
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
        "target_correspondence": Mock(),
        "frame_correspondee": frame_correspondee,
        "non_frame": Mock(),
        "non_frame_correspondee": Mock(),
    }
    builder = ChunkProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
