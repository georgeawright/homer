import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import WordBuilder, FunctionWordBuilder
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
        Mock(), Mock(), "word", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(word_concept)
    build_concept = Concept(
        Mock(), Mock(), "build", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), word_concept, build_concept, None, None, 1)
    word_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    text_concept = Concept(
        Mock(), Mock(), "text", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(text_concept)
    same_concept = Concept(
        Mock(), Mock(), "same", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(same_concept)
    input_concept = Concept(
        Mock(), Mock(), "input", None, None, None, "value", StructureCollection(), None
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
def target_view(bubble_chamber):
    members = Mock()
    parent_space = Mock()
    output_space = WorkingSpace(
        Mock(),
        Mock(),
        "output_space_name",
        bubble_chamber.concepts["text"],
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    quality = Mock()
    view = View(Mock(), Mock(), members, parent_space, output_space, quality)
    bubble_chamber.spaces.add(output_space)
    return view


@pytest.fixture
def temperature_conceptual_space(bubble_chamber):
    space = ConceptualSpace(
        Mock(), Mock(), "temperature", Mock(), [], StructureCollection(), 1, [], []
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
def target_correspondence(
    temperature_template_space,
    temperature_input_space,
    template,
    input_space,
    warm_concept,
    warm_lexeme,
):
    start = TemplateSlot(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        WordForm.HEADWORD,
        [Location([0], template), Location([0], temperature_template_space)],
    )
    end = Chunk(
        Mock(),
        Mock(),
        Mock(),
        [Location([], input_space), Location([0], temperature_input_space)],
        Mock(),
        input_space,
        Mock(),
    )
    end_label = Label(Mock(), Mock(), end, warm_concept, input_space, 1)
    end.links_out.add(end_label)
    start_space = temperature_template_space
    end_space = temperature_input_space
    parent_concept = Mock()
    parent_space = Mock()
    conceptual_space = Mock()
    quality = Mock()
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        Location([], parent_space),
        start_space,
        end_space,
        parent_concept,
        conceptual_space,
        quality,
    )
    correspondence._activation = 1.0
    return correspondence


def test_successful_adds_member_to_chunk_and_spawns_follow_up_and_same_chunk_cannot_be_recreated(
    bubble_chamber, target_view, target_correspondence
):
    parent_id = ""
    urgency = 1.0

    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, target_correspondence, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Word)
    assert isinstance(builder.child_codelets[0], FunctionWordBuilder)
    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, target_correspondence, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
