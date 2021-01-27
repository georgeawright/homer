import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import WordBuilder
from homer.codelets.evaluators import WordEvaluator
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept, Lexeme
from homer.structures.chunks import View, Word
from homer.structures.chunks.slots import TemplateSlot
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.structures.spaces.frames import Template
from homer.word_form import WordForm


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    word_concept = Concept(
        Mock(),
        Mock(),
        "word",
        None,
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
        None,
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
        None,
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
        None,
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
        None,
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
    lexeme = Lexeme(Mock(), Mock(), Mock(), {WordForm.HEADWORD: "warm"})
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
    template = Template(Mock(), Mock(), name, parent_concept, [], contents)
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
def template_slot(template, temperature_template_space, temperature_concept):
    slot = TemplateSlot(
        Mock(),
        Mock(),
        template,
        temperature_concept,
        WordForm.HEADWORD,
        [Location([0], template), Location([0], temperature_template_space)],
    )
    return slot


@pytest.fixture
def template_word(template, temperature_template_space):
    word = Word(Mock(), Mock(), "it", None, Location([1], template), template, 1.0)
    return word


@pytest.fixture
def input_chunk(input_space, temperature_input_space, warm_concept):
    chunk = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([], input_space), Location([0], temperature_input_space)],
        Mock(),
        input_space,
        Mock(),
    )
    label = Label(Mock(), Mock(), chunk, warm_concept, input_space, 1)
    chunk.links_out.add(label)
    return chunk


@pytest.fixture
def target_correspondence(
    template_slot,
    input_chunk,
    temperature_template_space,
    temperature_input_space,
    template,
    input_space,
    warm_concept,
    warm_lexeme,
):
    start_space = temperature_template_space
    end_space = temperature_input_space
    parent_concept = Mock()
    parent_space = Mock()
    conceptual_space = Mock()
    quality = Mock()
    correspondence = Correspondence(
        Mock(),
        Mock(),
        template_slot,
        input_chunk,
        Location([], parent_space),
        start_space,
        end_space,
        parent_concept,
        conceptual_space,
        quality,
    )
    correspondence._activation = 1.0
    return correspondence


@pytest.fixture
def target_view(bubble_chamber, target_correspondence, input_space, template):
    members = StructureCollection({target_correspondence})
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
    return view


def test_successful_creates_word_and_spawns_follow_up_and_same_word_cannot_be_recreated(
    bubble_chamber, target_view, template_slot
):
    parent_id = ""
    urgency = 1.0

    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, template_slot, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Word)
    assert isinstance(builder.child_codelets[0], WordEvaluator)
    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, template_slot, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result


def test_successful_creates_function_word_and_spawns_follow_up_and_same_word_cannot_be_recreated(
    bubble_chamber, target_view, template_word
):
    parent_id = ""
    urgency = 1.0

    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, template_word, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Word)
    assert isinstance(builder.child_codelets[0], WordEvaluator)
    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, template_word, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
