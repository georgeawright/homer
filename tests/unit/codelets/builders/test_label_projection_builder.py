import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import LabelProjectionBuilder
from homer.codelets.evaluators import LabelEvaluator
from homer.structure_collection import StructureCollection


@pytest.fixture
def target_view():
    view = Mock()
    existing_correspondence = Mock()
    existing_correspondence.name = "existing correspondence"
    existing_chunk = Mock()
    existing_word = Mock()
    existing_correspondence.arguments = StructureCollection(
        {existing_chunk, existing_word}
    )
    potential_label_word = Mock()
    potential_label_word.has_correspondence_to_space.return_value = False
    existing_word.potential_labeling_words = StructureCollection({potential_label_word})
    existing_correspondence.arguments = StructureCollection(
        {existing_chunk, existing_word}
    )
    existing_chunk.correspondences_to_space.return_value = StructureCollection(
        {existing_correspondence}
    )
    view.interpretation_space.contents.of_type.return_value = StructureCollection(
        {existing_chunk}
    )
    return view


@pytest.fixture
def bubble_chamber(target_view):
    chamber = Mock()
    chamber.concepts = {
        "build": Mock(),
        "label": Mock(),
        "noun": Mock(),
        "same": Mock(),
        "text": Mock(),
    }
    chamber.monitoring_views = StructureCollection({target_view})
    return chamber


@pytest.fixture
def parent_concept(bubble_chamber):
    concept = Mock()
    bubble_chamber.spaces = {"label concepts": [concept]}
    target_space = Mock()
    target_space.parent_concept.relevant_value = "value"
    target_space.contents = StructureCollection()
    concept.parent_space.instance_in_space.return_value = target_space
    return concept


@pytest.fixture
def target_word(bubble_chamber, parent_concept):
    word = Mock()
    word.lexeme.concepts.get_random.return_value = parent_concept
    return word


def test_successful_creates_label_corresponding_to_word_and_spawns_follow_up(
    bubble_chamber, target_view, target_word
):
    target_chunk = Mock()
    target_chunk.has_label.return_value = False
    target_word.has_correspondence_to_space.return_value = False
    builder = LabelProjectionBuilder(
        "", "", bubble_chamber, target_view, target_chunk, target_word, 1
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert len(builder.child_codelets) == 1
    assert isinstance(builder.child_codelets[0], LabelEvaluator)


def test_fizzles_if_target_word_already_has_correspondence_in_interpretation(
    bubble_chamber, target_view, target_word
):
    target_chunk = Mock()
    target_chunk.has_label.return_value = False
    target_word.has_correspondence_to_space.return_value = True
    builder = LabelProjectionBuilder(
        "", "", bubble_chamber, target_view, target_chunk, target_word, 1
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
    assert len(builder.child_codelets) == 1
    assert isinstance(builder.child_codelets[0], LabelProjectionBuilder)


def test_fizzles_if_target_chunk_already_has_corresponding_label(
    bubble_chamber, target_view, target_word
):
    target_chunk = Mock()
    target_chunk.has_label.return_value = True
    target_word.has_correspondence_to_space.return_value = True
    builder = LabelProjectionBuilder(
        "", "", bubble_chamber, target_view, target_chunk, target_word, 1
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
    assert len(builder.child_codelets) == 1
    assert isinstance(builder.child_codelets[0], LabelProjectionBuilder)
