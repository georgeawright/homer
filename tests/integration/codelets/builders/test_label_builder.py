import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import ProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.builders import LabelBuilder
from homer.codelets.evaluators import LabelEvaluator
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.links import Label, Relation
from homer.structures.spaces import ConceptualSpace, WorkingSpace


@pytest.fixture
def label_concepts_space():
    space = ConceptualSpace(
        Mock(),
        Mock(),
        "label concepts",
        Mock(),
        [],
        StructureCollection(),
        Mock(),
        Mock(),
        Mock(),
    )
    return space


@pytest.fixture
def top_level_working_space():
    space = WorkingSpace(
        Mock(),
        Mock(),
        "top level working",
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def temperature_concept(label_concepts_space):
    concept = Concept(
        Mock(),
        Mock(),
        "temperature",
        None,
        None,
        label_concepts_space,
        Mock(),
        "value",
        StructureCollection(),
        math.dist,
    )
    label_concepts_space.contents.add(concept)
    return concept


@pytest.fixture
def temperature_space(temperature_concept):
    space = ConceptualSpace(
        "temperature",
        Mock(),
        "temperature",
        temperature_concept,
        [],
        StructureCollection(),
        1,
        [],
        [],
    )
    temperature_concept.child_spaces.add(space)
    return space


@pytest.fixture
def mild_concept(temperature_space):
    classifier = ProximityClassifier()
    mild = Concept(
        Mock(),
        Mock(),
        "mild",
        [10],
        classifier,
        temperature_space,
        Mock(),
        "value",
        StructureCollection(),
        math.dist,
    )
    temperature_space.contents.add(mild)
    return mild


@pytest.fixture
def bubble_chamber(mild_concept, label_concepts_space, top_level_working_space):
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
        Mock(),
    )
    chamber.concepts.add(mild_concept)
    chamber.conceptual_spaces.add(label_concepts_space)
    chamber.working_spaces.add(top_level_working_space)
    label_concept = Concept(
        Mock(),
        Mock(),
        "label",
        None,
        None,
        None,
        Mock(),
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(label_concept)
    build_concept = Concept(
        Mock(),
        Mock(),
        "build",
        None,
        None,
        None,
        Mock(),
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), label_concept, build_concept, None, None, 1)
    label_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def target_chunk(bubble_chamber):
    location_concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        "coordinates",
        Mock(),
        math.dist,
    )
    input_space = WorkingSpace(
        Mock(),
        Mock(),
        "input",
        location_concept,
        [],
        StructureCollection(),
        Mock(),
        Mock(),
        Mock(),
    )
    parent_spaces = StructureCollection({input_space})
    chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        [Location([0, 0], input_space)],
        StructureCollection(),
        0.0,
    )
    second_chunk = Chunk(
        Mock(),
        Mock(),
        [10],
        [Location([0, 1], input_space)],
        StructureCollection(),
        0.0,
    )
    bubble_chamber.chunks.add(chunk)
    bubble_chamber.chunks.add(second_chunk)
    input_space.contents.add(chunk)
    input_space.contents.add(second_chunk)
    chunk.parent_spaces.add(input_space)
    return chunk


def test_successful_adds_label_to_chunk_and_spawns_follow_up_and_same_label_cannot_be_recreated(
    bubble_chamber, target_chunk
):
    parent_id = ""
    urgency = 1.0

    builder = LabelBuilder.spawn(parent_id, bubble_chamber, target_chunk, urgency)
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Label)
    assert isinstance(builder.child_codelets[0], LabelEvaluator)
    builder = LabelBuilder.spawn(parent_id, bubble_chamber, target_chunk, urgency)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
