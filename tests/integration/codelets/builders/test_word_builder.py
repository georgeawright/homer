import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import WordBuilder
from homer.codelets.evaluators import WordEvaluator
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Word
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.structures.spaces.frames import Template
from homer.tools import hasinstance
from homer.word_form import WordForm


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    word_concept = Concept(
        Mock(),
        Mock(),
        "word",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(word_concept)
    build_concept = Concept(
        Mock(),
        Mock(),
        "build",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), word_concept, build_concept, None, None, 1)
    word_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    text_concept = Concept(
        Mock(),
        Mock(),
        "text",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(text_concept)
    same_concept = Concept(
        Mock(),
        Mock(),
        "same",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(same_concept)
    input_concept = Concept(
        Mock(),
        Mock(),
        "input",
        Mock(),
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(input_concept)
    top_level_working_space = WorkingSpace(
        Mock(),
        Mock(),
        "top level working",
        None,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    chamber.working_spaces.add(top_level_working_space)
    return chamber


@pytest.fixture
def temperature_concept(bubble_chamber):
    concept = Concept(
        Mock(),
        Mock(),
        "temperature",
        Mock(),
        Mock(),
        "value",
        Mock(),
        StructureCollection(),
        Mock(),
    )
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def temperature_conceptual_space(bubble_chamber, temperature_concept):
    space = ConceptualSpace(
        Mock(),
        Mock(),
        "temperature",
        temperature_concept,
        [],
        StructureCollection(),
        1,
        [],
        [],
    )
    return space


@pytest.fixture
def warm_concept(temperature_conceptual_space, bubble_chamber):
    concept = Concept(
        Mock(),
        Mock(),
        "warm",
        Location([16], temperature_conceptual_space),
        Mock(),
        "value",
        Mock(),
        StructureCollection(),
        Mock(),
    )
    bubble_chamber.concepts.add(concept)
    temperature_conceptual_space.add(concept)
    return concept


@pytest.fixture
def warm_lexeme(warm_concept):
    lexeme = Lexeme(Mock(), Mock(), Mock(), {WordForm.HEADWORD: "warm"}, Mock())
    concept_to_lexeme_relation = Relation(
        Mock(), Mock(), warm_concept, lexeme, None, None, None
    )
    warm_concept.links_out.add(concept_to_lexeme_relation)
    lexeme.links_in.add(concept_to_lexeme_relation)
    return lexeme


@pytest.fixture
def template(bubble_chamber):
    name = "mock template"
    contents = StructureCollection()
    parent_concept = bubble_chamber.concepts["text"]
    template = Template(Mock(), Mock(), name, parent_concept, Mock(), [], contents)
    word_form = Mock()
    lexeme = Lexeme(Mock(), Mock(), Mock(), {word_form: Mock()}, Mock())
    slot = Word(Mock(), Mock(), lexeme, word_form, Mock(), Mock(), Mock(), Mock())
    template.contents.add(slot)
    bubble_chamber.frames.add(template)
    return template


@pytest.fixture
def temperature_template_space(template, temperature_conceptual_space):
    temperature_space = temperature_conceptual_space.instance_in_space(template)
    template.add(temperature_space)
    return temperature_space


@pytest.fixture
def input_space(bubble_chamber):
    name = "input space"
    contents = StructureCollection()
    parent_concept = bubble_chamber.concepts["input"]
    space = WorkingSpace(
        Mock(), Mock(), name, parent_concept, Mock(), [], contents, 0, [], []
    )
    bubble_chamber.working_spaces.add(space)
    return space


@pytest.fixture
def temperature_input_space(input_space, temperature_conceptual_space):
    temperature_space = temperature_conceptual_space.instance_in_space(input_space)
    input_space.add(temperature_space)
    return temperature_space


@pytest.fixture
def target_view(bubble_chamber, input_space, template):
    members = StructureCollection()
    location = Mock()
    input_spaces = StructureCollection({input_space, template})
    output_space = WorkingSpace(
        Mock(),
        Mock(),
        "output_space_name",
        bubble_chamber.concepts["text"],
        Mock(),
        [],
        StructureCollection(),
        1,
        [],
        [],
    )
    quality = Mock()
    view = View(Mock(), Mock(), location, members, input_spaces, output_space, quality)
    bubble_chamber.spaces.add(output_space)
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def input_space_chunk(input_space, temperature_input_space, warm_concept, warm_lexeme):
    chunk = Chunk(
        "input space chunk",
        Mock(),
        Mock(),
        [Location([], input_space), Location([0], temperature_input_space)],
        Mock(),
        input_space,
        Mock(),
    )
    label = Label(
        "input chunk label", Mock(), chunk, warm_concept, temperature_input_space, 1
    )
    input_space.add(chunk)
    temperature_input_space.add(chunk)
    temperature_input_space.add(label)
    chunk.links_out.add(label)
    return chunk


@pytest.fixture
def template_chunk(
    bubble_chamber,
    warm_concept,
    template,
    temperature_template_space,
    temperature_input_space,
    input_space_chunk,
    target_view,
):
    chunk = Chunk(
        "template chunk",
        Mock(),
        None,
        [Location([], template), Location([], temperature_template_space)],
        StructureCollection(),
        template,
        1,
    )
    label = Label(
        "template chunk label", Mock(), chunk, None, temperature_template_space, 1
    )
    target_view.slot_values[label.structure_id] = warm_concept
    chunk.links_out.add(label)
    input_chunk_label = input_space_chunk.labels.get_random()
    input_to_template_chunk_correspondence = Correspondence(
        "input_to_template_chunk_correspondence",
        Mock(),
        input_chunk_label,
        label,
        temperature_input_space,
        temperature_template_space,
        [Location([], input_space_chunk), Location([], temperature_template_space)],
        bubble_chamber.concepts["same"],
        temperature_template_space,
        target_view,
        1,
    )
    input_chunk_label.links_in.add(input_to_template_chunk_correspondence)
    input_chunk_label.links_out.add(input_to_template_chunk_correspondence)
    label.links_in.add(input_to_template_chunk_correspondence)
    label.links_out.add(input_to_template_chunk_correspondence)
    target_view.members.add(input_to_template_chunk_correspondence)
    return chunk


@pytest.fixture
def template_slot_word(
    bubble_chamber, template_chunk, template, temperature_template_space, target_view
):
    slot = Word(
        "template_slot_word",
        Mock(),
        None,
        WordForm.HEADWORD,
        Location([0], template),
        template,
        Mock(),
    )
    label = template_chunk.labels.get_random()
    label_to_slot_correspondence = Correspondence(
        "label to slot word correspondence",
        Mock(),
        label,
        slot,
        temperature_template_space,
        template,
        [
            label.location_in_space(temperature_template_space),
            slot.location_in_space(template),
        ],
        bubble_chamber.concepts["same"],
        temperature_conceptual_space,
        target_view,
        1,
        is_privileged=True,
    )
    slot.links_in.add(label_to_slot_correspondence)
    slot.links_out.add(label_to_slot_correspondence)
    label.links_in.add(label_to_slot_correspondence)
    label.links_out.add(label_to_slot_correspondence)
    target_view.members.add(label_to_slot_correspondence)
    return slot


@pytest.fixture
def template_function_word(template):
    it_lexeme = Lexeme(Mock(), Mock(), "it", {WordForm.HEADWORD: "it"}, Mock())
    word = Word(
        Mock(),
        Mock(),
        it_lexeme,
        WordForm.HEADWORD,
        Location([1], template),
        template,
        1.0,
    )
    return word


def test_successful_creates_word_and_spawns_follow_up_and_same_word_cannot_be_recreated(
    bubble_chamber, target_view, template_slot_word
):
    parent_id = ""
    urgency = 1.0
    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, template_slot_word, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert hasinstance(builder.child_structures, Word)
    assert isinstance(builder.child_codelets[0], WordEvaluator)
    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, template_slot_word, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result


def test_successful_creates_function_word_and_spawns_follow_up_and_same_word_cannot_be_recreated(
    bubble_chamber, target_view, template_function_word
):
    parent_id = ""
    urgency = 1.0
    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, template_function_word, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert hasinstance(builder.child_structures, Word)
    assert isinstance(builder.child_codelets[0], WordEvaluator)
    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, template_function_word, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
