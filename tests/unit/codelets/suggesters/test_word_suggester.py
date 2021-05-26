import pytest
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders import WordBuilder
from homer.codelets.suggesters import WordSuggester
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Word
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"suggest": Mock(), "same": Mock(), "word": Mock()}
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
def warm_lexeme():
    lexeme = Mock()
    return lexeme


@pytest.fixture
def warm_concept(temperature_space, warm_lexeme):
    concept = Mock()
    concept.parent_space = temperature_space
    concept.lexemes = StructureCollection({warm_lexeme})
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
    is_lexeme = Mock()
    word = Mock()
    word.lexeme = is_lexeme
    word.word_form = Mock()
    is_lexeme.forms = {word.word_form: Mock()}
    word.is_slot = False
    word.parent_space = frame
    word.has_correspondence_to_space.return_value = False
    word.location_in_space.return_value = Location([0], frame)
    word.correspondences = StructureCollection()
    return word


@pytest.fixture
def frame_slot(frame, temperature_concept, warm_lexeme):
    slot = Mock()
    slot.name = "frame slot"
    slot.is_slot = True
    slot.parent_space = frame
    slot.value = temperature_concept
    slot.word_form = Mock()
    warm_lexeme.forms = {slot.word_form: Mock()}
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
def frame_chunk_label(warm_concept):
    label = Mock()
    label.name = "frame chunk label"
    label.is_word = False
    label.parent_concept = warm_concept
    label.correspondences = StructureCollection()
    return label


@pytest.fixture
def frame_chunk(frame_chunk_label, input_space):
    chunk = Mock()
    chunk.location_in_space.return_value = Location([1], input_space)
    chunk.labels = StructureCollection({frame_chunk_label})
    return chunk


@pytest.fixture
def input_label(temperature_space_in_input, frame_chunk_label):
    label = Mock()
    label.is_word = False
    label.correspondences = StructureCollection()
    return label


@pytest.fixture
def input_to_frame_correspondence(input_label, frame_chunk_label):
    correspondence = Mock()
    correspondence.name = "input to frame"
    correspondence.start = input_label
    correspondence.end = frame_chunk_label
    correspondence.activation = 1
    input_label.correspondences.add(correspondence)
    frame_chunk_label.correspondences.add(correspondence)
    return correspondence


@pytest.fixture
def label_slot_correspondence(
    frame_slot,
    frame_chunk_label,
    temperature_space_in_frame,
    temperature_space_in_input,
    input_label,
):
    correspondence = Mock()
    correspondence.start = frame_slot
    correspondence.end = frame_chunk_label
    correspondence.start_space = temperature_space_in_frame
    correspondence.end_space = temperature_space_in_input
    correspondence.activation = 1.0
    correspondence.is_privileged = False
    frame_slot.correspondences = StructureCollection({correspondence})
    frame_chunk_label.correspondences.add(correspondence)
    return correspondence


@pytest.fixture
def target_view(
    input_space,
    output_space,
    frame_chunk_label,
    label_slot_correspondence,
    warm_concept,
    input_to_frame_correspondence,
):
    view = Mock()
    view.input_spaces.of_type.return_value = input_space
    view.output_space = output_space
    view.members = StructureCollection(
        {label_slot_correspondence, input_to_frame_correspondence}
    )
    view.slot_values = {frame_chunk_label.structure_id: warm_concept}
    return view


def test_suggests_word_from_slot(bubble_chamber, target_view, frame_slot):
    target_structures = {"target_view": target_view, "target_word": frame_slot}
    word_suggester = WordSuggester(Mock(), Mock(), bubble_chamber, target_structures, 1)
    result = word_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert 1 == len(word_suggester.child_codelets)
    assert isinstance(word_suggester.child_codelets[0], WordBuilder)


def test_suggests_word_from_word(bubble_chamber, target_view, frame_word):
    target_structures = {"target_view": target_view, "target_word": frame_word}
    word_suggester = WordSuggester(Mock(), Mock(), bubble_chamber, target_structures, 1)
    result = word_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert 1 == len(word_suggester.child_codelets)
    assert isinstance(word_suggester.child_codelets[0], WordBuilder)
