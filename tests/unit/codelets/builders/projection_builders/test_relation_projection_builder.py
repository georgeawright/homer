import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.projection_builders import RelationProjectionBuilder
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence
from homer.structures.nodes import Word
from homer.tools import hasinstance


@pytest.fixture
def grammar_space(bubble_chamber):
    space = Mock()
    space.name = "grammar"
    bubble_chamber.conceptual_spaces = bubble_chamber.new_structure_collection(space)
    return space


@pytest.fixture
def target_view():
    view = Mock()
    view.slot_values = {}
    return view


@pytest.fixture
def target_projectee(target_view):
    relation = Mock()
    relation.start = Mock()
    relation.start.correspondences_to_space.return_value = Mock()
    return relation


@pytest.fixture
def relation_concept():
    concept = Mock()
    return concept


@pytest.fixture
def frame_correspondee(bubble_chamber, target_view, relation_concept, target_projectee):
    correspondee = Mock()
    correspondee.structure_id = "frame_correspondee"
    frame_correspondence = Mock()
    frame_correspondence.start = frame_correspondee
    frame_correspondence.end = target_projectee
    target_projectee.correspondences = bubble_chamber.new_structure_collection(
        frame_correspondence
    )
    non_frame_correspondee = Mock()
    non_frame_correspondence = Mock()
    non_frame_correspondence.start = non_frame_correspondee
    non_frame_correspondence.end = correspondee
    correspondee.correspondences = bubble_chamber.new_structure_collection(
        frame_correspondence, non_frame_correspondence
    )
    target_view.members = bubble_chamber.new_structure_collection(
        frame_correspondence, non_frame_correspondence
    )
    target_view.slot_values[correspondee.structure_id] = relation_concept
    return correspondee


def test_projects_slot_into_output_space(
    bubble_chamber, target_view, target_projectee, frame_correspondee, grammar_space
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
    builder = RelationProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
    builder.run()
    assert CodeletResult.SUCCESS == builder.result


def test_fizzles_if_word_projection_exists(
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
    builder = RelationProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
