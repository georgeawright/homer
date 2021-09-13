import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.projection_builders import WordProjectionBuilder
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence
from homer.structures.nodes import Word
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"build": Mock(), "same": Mock(), "word": Mock()}
    chamber.conceptual_spaces = {"grammar": Mock()}
    chamber.words = StructureCollection()
    return chamber


@pytest.fixture
def target_view():
    view = Mock()
    view.slot_values = {}
    return view


@pytest.fixture
def target_projectee(target_view):
    word = Mock()
    word_copy = Mock()
    word_copy.locations = []
    word.copy_to_location.return_value = word_copy
    frame_correspondee = Mock()
    frame_correspondee.structure_id = "frame_correspondee"
    frame_correspondence = Mock()
    frame_correspondence.start = frame_correspondee
    frame_correspondence.end = word
    word.correspondences = StructureCollection({frame_correspondence})
    non_frame_correspondee = Mock()
    non_frame_correspondence = Mock()
    non_frame_correspondence.start = non_frame_correspondee
    non_frame_correspondence.end = frame_correspondee
    frame_correspondee.correspondences = StructureCollection({non_frame_correspondence})
    target_view.members = StructureCollection(
        {frame_correspondence, non_frame_correspondence}
    )
    target_view.slot_values[frame_correspondee.structure_id] = Mock()
    return word


@pytest.fixture
def abstract_word(bubble_chamber):
    word = Mock()
    word.name = "word"
    bubble_chamber.words.add(word)
    word_copy = Mock()
    word_copy.locations = []
    word.copy_to_location.return_value = word_copy
    return word


@pytest.fixture
def lexeme(abstract_word, target_projectee):
    lexeme = Mock()
    lexeme.word_forms = {target_projectee.word_form: abstract_word.name}
    return lexeme


@pytest.fixture
def word_concept(lexeme):
    concept = Mock()
    concept.lexemes = StructureCollection({lexeme})
    return concept


@pytest.fixture
def frame_correspondee(target_view, word_concept):
    correspondee = Mock()
    target_view.slot_values[correspondee.structure_id] = word_concept
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
    builder = WordProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
    builder.run()
    assert CodeletResult.SUCCESS == builder.result


def test_projects_non_slot_word_into_output_space(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.is_slot = False
    target_projectee.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
        "target_correspondence": Mock(),
        "frame_correspondee": frame_correspondee,
        "non_frame": Mock(),
        "non_frame_correspondee": Mock(),
    }
    builder = WordProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
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
    builder = WordProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
