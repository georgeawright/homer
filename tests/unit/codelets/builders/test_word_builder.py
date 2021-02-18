import pytest
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders import WordBuilder
from homer.codelets.evaluators import WordEvaluator
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunks import Word
from homer.structures.chunks.slots import TemplateSlot


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"build": Mock(), "same": Mock(), "word": Mock()}
    space = Mock()
    space.sub_spaces = [Mock(), Mock()]
    chamber.get_super_space.return_value = space
    return chamber


@pytest.fixture
def temperature_concept():
    concept = Mock()
    return concept


@pytest.fixture
def temperature_space(temperature_concept):
    space = Mock()
    space.parent_concept = temperature_concept
    return space


@pytest.fixture
def warm_concept(temperature_space):
    concept = Mock()
    concept.parent_space = temperature_space
    return concept


@pytest.fixture
def frame():
    frame = Mock()
    return frame


@pytest.fixture
def temperature_space_in_frame(temperature_space):
    space = Mock()
    space.conceptual_space = temperature_space
    return space


@pytest.fixture
def frame_word(frame):
    word = Mock()
    word.parent_space = frame
    word.has_correspondence_to_space.return_value = False
    word.location_in_space.return_value = Location([0], frame)
    return word


@pytest.fixture
def frame_slot(frame, temperature_concept):
    slot = TemplateSlot(Mock(), Mock(), Mock(), Mock(), Mock(), [Location([0], frame)])
    slot.parent_space = frame
    slot.value = temperature_concept
    return slot


@pytest.fixture
def input_space():
    space = Mock()
    return space


@pytest.fixture
def temperature_space_in_input(temperature_space):
    space = Mock()
    space.conceptual_space = temperature_space
    return space


@pytest.fixture
def output_space():
    space = Mock()
    return space


@pytest.fixture
def input_space_chunk_label(warm_concept):
    label = Mock()
    label.parent_concept = warm_concept
    return label


@pytest.fixture
def input_space_chunk(input_space_chunk_label, input_space):
    chunk = Mock()
    chunk.location_in_space.return_value = Location([1], input_space)
    chunk.labels = StructureCollection({input_space_chunk_label})
    return chunk


@pytest.fixture
def chunk_slot_correspondence(
    frame_slot,
    input_space_chunk,
    temperature_space_in_frame,
    temperature_space_in_input,
):
    correspondence = Mock()
    correspondence.start = frame_slot
    correspondence.end = input_space_chunk
    correspondence.start_space = temperature_space_in_frame
    correspondence.end_space = temperature_space_in_input
    correspondence.activation = 1.0
    correspondence.get_non_slot_argument.return_value = input_space_chunk
    correspondence.is_privileged = False
    return correspondence


@pytest.fixture
def target_view(input_space, output_space, chunk_slot_correspondence):
    view = Mock()
    view.input_spaces.of_type.return_value = input_space
    view.output_space = output_space
    view.members = StructureCollection({chunk_slot_correspondence})
    return view


def test_successfully_creates_word_from_slot(bubble_chamber, target_view, frame_slot):
    word_builder = WordBuilder(
        Mock(), Mock(), bubble_chamber, target_view, frame_slot, 1
    )
    result = word_builder.run()
    assert CodeletResult.SUCCESS == result
    assert isinstance(word_builder.child_structure, Word)
    assert 1 == len(word_builder.child_codelets)
    assert isinstance(word_builder.child_codelets[0], WordEvaluator)


def test_successfully_creates_word_from_word(bubble_chamber, target_view, frame_word):
    word_builder = WordBuilder(
        Mock(), Mock(), bubble_chamber, target_view, frame_word, 1
    )
    result = word_builder.run()
    assert CodeletResult.SUCCESS == result
    assert isinstance(word_builder.child_structure, Word)
    assert 1 == len(word_builder.child_codelets)
    assert isinstance(word_builder.child_codelets[0], WordEvaluator)
