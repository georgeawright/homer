import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import (
    DifferenceClassifier,
    ProximityClassifier,
    SamenessClassifier,
)
from homer.codelet_result import CodeletResult
from homer.codelets.builders import CorrespondenceBuilder
from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.nodes import Chunk, Concept, Word
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.spaces import ConceptualSpace, Frame, WorkingSpace
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
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    correspondence_concept = Concept(
        Mock(),
        Mock(),
        "correspondence",
        Mock(),
        None,
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(correspondence_concept)
    build_concept = Concept(
        Mock(),
        Mock(),
        "build",
        Mock(),
        None,
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(build_concept)
    relation = Relation(
        Mock(), Mock(), correspondence_concept, build_concept, None, None, 1
    )
    text_concept = Concept(
        Mock(),
        Mock(),
        "text",
        Mock(),
        None,
        None,
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(text_concept)
    text_conceptual_space = ConceptualSpace(
        "text", Mock(), "text", None, [], StructureCollection(), 1, [], []
    )
    chamber.conceptual_spaces.add(text_conceptual_space)
    correspondence_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    label_concepts_space = ConceptualSpace(
        "label concepts",
        Mock(),
        "label concepts",
        None,
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    chamber.conceptual_spaces.add(label_concepts_space)
    correspondential_concepts_space = ConceptualSpace(
        "correspondential concepts",
        Mock(),
        "correspondential concepts",
        None,
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    chamber.conceptual_spaces.add(correspondential_concepts_space)
    top_level_space = ConceptualSpace(
        "top level",
        Mock(),
        "top level",
        None,
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    chamber.conceptual_spaces.add(top_level_space)
    chamber.working_spaces.add(
        top_level_space.instance_in_space(None, name="top level working")
    )
    return chamber


@pytest.fixture
def same_different_concept(bubble_chamber):
    same_different = Concept(
        Mock(),
        Mock(),
        "same",
        Location([], bubble_chamber.spaces["correspondential concepts"]),
        Mock(),
        "value",
        Mock(),
        StructureCollection(),
        math.dist,
    )
    bubble_chamber.concepts.add(same_different)
    bubble_chamber.spaces["correspondential concepts"].add(same_different)
    return same_different


@pytest.fixture
def same_different_space(same_different_concept, bubble_chamber):
    space = ConceptualSpace(
        "same-different",
        Mock(),
        "same-different",
        same_different_concept,
        [Location([], bubble_chamber.spaces["correspondential concepts"])],
        StructureCollection(),
        1,
        [],
        [],
    )
    bubble_chamber.conceptual_spaces.add(space)
    bubble_chamber.spaces["correspondential concepts"].add(space)
    return space


@pytest.fixture
def same_concept(same_different_space, bubble_chamber):
    concept = Concept(
        Mock(),
        Mock(),
        "same",
        Location([1], same_different_space),
        SamenessClassifier(),
        "value",
        Mock(),
        StructureCollection(),
        math.dist,
    )
    same_different_space.add(concept)
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def temperature_concept(bubble_chamber):
    temperature = Concept(
        Mock(),
        Mock(),
        "temperature",
        Location([], bubble_chamber.spaces["label concepts"]),
        Mock(),
        "value",
        Mock(),
        StructureCollection(),
        math.dist,
    )
    bubble_chamber.concepts.add(temperature)
    bubble_chamber.spaces["label concepts"].add(temperature)
    return temperature


@pytest.fixture
def temperature_conceptual_space(temperature_concept, bubble_chamber):
    space = ConceptualSpace(
        "temperature",
        Mock(),
        "temperature",
        temperature_concept,
        [Location([], bubble_chamber.spaces["label concepts"])],
        StructureCollection(),
        1,
        [],
        [],
    )
    temperature_concept.child_spaces.add(space)
    bubble_chamber.conceptual_spaces.add(space)
    bubble_chamber.spaces["label concepts"].add(space)
    return space


@pytest.fixture
def mild_concept(temperature_conceptual_space, bubble_chamber):
    concept = Concept(
        Mock(),
        Mock(),
        "mild",
        Location([10], temperature_conceptual_space),
        Mock(),
        "value",
        Mock(),
        StructureCollection(),
        math.dist,
    )
    temperature_conceptual_space.add(concept)
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture
def input_space():
    space = WorkingSpace(
        "input",
        Mock(),
        "input",
        Mock(),
        None,
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def temperature_working_space(
    temperature_conceptual_space, input_space, bubble_chamber
):
    working_space = temperature_conceptual_space.instance_in_space(input_space)
    bubble_chamber.working_spaces.add(working_space)
    return working_space


@pytest.fixture
def templates_space(bubble_chamber):
    space = ConceptualSpace(
        Mock(),
        Mock(),
        "templates",
        None,
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    bubble_chamber.conceptual_spaces.add(space)
    return space


@pytest.fixture
def template(templates_space, bubble_chamber):
    template = Template(
        Mock(),
        Mock(),
        "[temperature]",
        None,
        None,
        [Location([], templates_space)],
        StructureCollection(),
    )
    bubble_chamber.frames.add(template)
    return template


@pytest.fixture
def temperature_template_space(
    temperature_concept, temperature_conceptual_space, template, bubble_chamber
):
    space = WorkingSpace(
        Mock(),
        Mock(),
        "temperature space for template",
        temperature_concept,
        temperature_conceptual_space,
        [Location([], template)],
        StructureCollection(),
        1,
        [],
        [],
        is_basic_level=True,
    )
    template.add(space)
    bubble_chamber.working_spaces.add(space)
    return space


@pytest.fixture
def target_view(bubble_chamber, input_space, template):
    view = View(
        "target_view",
        Mock(),
        Mock(),
        StructureCollection(),
        StructureCollection({input_space, template}),
        Mock(),
        0,
    )
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def target_chunk(temperature_working_space, mild_concept, bubble_chamber):
    chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        [Location([10], temperature_working_space)],
        StructureCollection(),
        Mock(),
        1.0,
    )
    temperature_working_space.add(chunk)
    bubble_chamber.chunks.add(chunk)
    mild_label = Label(
        Mock(), Mock(), chunk, mild_concept, temperature_working_space, 1.0
    )
    bubble_chamber.labels.add(mild_label)
    chunk.links_out.add(mild_label)
    nearby_chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        [Location([10], temperature_working_space)],
        StructureCollection(),
        Mock(),
        1.0,
    )
    temperature_working_space.add(nearby_chunk)
    bubble_chamber.chunks.add(nearby_chunk)
    return chunk


@pytest.fixture
def target_slot(
    temperature_concept, template, temperature_template_space, bubble_chamber
):
    slot = Chunk(
        Mock(),
        Mock(),
        None,
        [Location([0], template), Location([], temperature_template_space)],
        StructureCollection(),
        template,
        1.0,
    )
    bubble_chamber.slots.add(slot)
    template.add(slot)
    temperature_template_space.add(slot)
    slot_label = Label(Mock(), Mock(), slot, None, temperature_template_space, 1.0)
    slot.links_out.add(slot_label)
    temperature_template_space.add(slot_label)
    bubble_chamber.labels.add(slot_label)
    return slot


def test_successful_adds_correspondence_to_chunk_and_spawns_follow_up_and_same_correspondence_cannot_be_recreated(
    bubble_chamber,
    target_view,
    temperature_working_space,
    target_chunk,
    target_slot,
    same_concept,
    mild_concept,
):
    target_label = target_chunk.labels.get_random()
    target_slot_label = target_slot.labels.get_random()
    builder = CorrespondenceBuilder.spawn(
        "", bubble_chamber, target_view, temperature_working_space, target_label, 1.0
    )
    builder.run()
    assert same_concept == builder.parent_concept
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Correspondence)
    assert isinstance(builder.child_codelets[0], CorrespondenceEvaluator)
    assert target_view.slot_values[target_slot_label.structure_id] == mild_concept.value
    builder.child_structure.quality = 1.0

    builder = CorrespondenceBuilder.spawn(
        "", bubble_chamber, target_view, temperature_working_space, target_chunk, 1.0
    )
    builder.run()
    assert same_concept == builder.parent_concept
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Correspondence)
    assert isinstance(builder.child_codelets[0], CorrespondenceEvaluator)

    builder = CorrespondenceBuilder.spawn(
        "", bubble_chamber, target_view, temperature_working_space, target_chunk, 1.0
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
