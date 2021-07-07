import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import ProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.builders import LabelBuilder
from homer.codelets.suggesters import LabelSuggester
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Label, Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.tools import centroid_euclidean_distance, hasinstance


@pytest.fixture
def label_concepts_space():
    space = ConceptualSpace(
        "label concepts",
        Mock(),
        "label concepts",
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def top_level_working_space():
    space = WorkingSpace(
        Mock(),
        Mock(),
        "top level working",
        Mock(),
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
        [Location([], label_concepts_space)],
        None,
        Chunk,
        Mock(),
        StructureCollection(),
        centroid_euclidean_distance,
    )
    label_concepts_space.contents.add(concept)
    return concept


@pytest.fixture
def temperature_space(label_concepts_space, temperature_concept):
    space = ConceptualSpace(
        "temperature",
        Mock(),
        "temperature",
        temperature_concept,
        [Location([], label_concepts_space)],
        StructureCollection(),
        1,
        [],
        [],
        is_basic_level=True,
    )
    label_concepts_space.add(space)
    temperature_concept.child_spaces.add(space)
    return space


@pytest.fixture
def mild_concept(temperature_space):
    classifier = ProximityClassifier()
    mild = Concept(
        Mock(),
        Mock(),
        "mild",
        [Location([[10]], temperature_space)],
        classifier,
        Chunk,
        temperature_space,
        StructureCollection(),
        centroid_euclidean_distance,
    )
    temperature_space.contents.add(mild)
    return mild


@pytest.fixture
def bubble_chamber(mild_concept, label_concepts_space, top_level_working_space):
    chamber = BubbleChamber.setup(Mock())
    text_concept = Mock()
    text_concept.name = "text"
    chamber.concepts.add(text_concept)
    chamber.concepts.add(mild_concept)
    chamber.conceptual_spaces.add(label_concepts_space)
    chamber.working_spaces.add(top_level_working_space)
    label_concept = Concept(
        Mock(),
        Mock(),
        "label",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(label_concept)
    suggest_concept = Concept(
        Mock(),
        Mock(),
        "suggest",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(suggest_concept)
    relation = Relation(Mock(), Mock(), label_concept, suggest_concept, None, None, 1)
    label_concept.links_out.add(relation)
    suggest_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def target_chunk(bubble_chamber, temperature_space):
    input_concept = Concept(
        Mock(),
        Mock(),
        "input",
        Mock(),
        Mock(),
        "coordinates",
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    bubble_chamber.concepts.add(input_concept)
    input_space = WorkingSpace(
        Mock(),
        Mock(),
        "input",
        input_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    temperature_space_in_input = temperature_space.instance_in_space(input_space)
    chunk = Chunk(
        Mock(),
        Mock(),
        [Location([0, 0], input_space), Location([[10]], temperature_space_in_input)],
        StructureCollection(),
        input_space,
        0.0,
    )
    second_chunk = Chunk(
        Mock(),
        Mock(),
        [Location([[0, 1]], input_space), Location([[10]], temperature_space_in_input)],
        StructureCollection(),
        Mock(),
        0.0,
    )
    bubble_chamber.chunks.add(chunk)
    bubble_chamber.chunks.add(second_chunk)
    input_space.contents.add(chunk)
    input_space.contents.add(second_chunk)
    chunk.parent_spaces.add(input_space)
    return chunk


def test_gives_high_confidence_for_compatible_chunk_and_spawns_follow_up(
    bubble_chamber, target_chunk
):
    parent_id = ""
    urgency = 1.0

    suggester = LabelSuggester.spawn(
        parent_id,
        bubble_chamber,
        {"target_node": target_chunk, "parent_concept": None},
        urgency,
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert isinstance(suggester.child_codelets[0], LabelBuilder)
