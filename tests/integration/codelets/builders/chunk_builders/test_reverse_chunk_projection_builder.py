import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import ProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.builders.chunk_builders import ReverseChunkProjectionBuilder
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Label, Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.structures.views import MonitoringView
from homer.tools import centroid_euclidean_distance, hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber.setup(Mock())
    chunk_concept = Concept(
        Mock(),
        Mock(),
        "chunk",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(chunk_concept)
    build_concept = Concept(
        Mock(),
        Mock(),
        "build",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), chunk_concept, build_concept, None, None, 1)
    chunk_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    same_concept = Concept(
        Mock(),
        Mock(),
        "same",
        Mock(),
        None,
        "value",
        Mock(),
        StructureCollection(),
        None,
    )
    chamber.concepts.add(same_concept)
    return chamber


@pytest.fixture
def temperature_concept():
    concept = Concept(
        "",
        "",
        "temperature",
        Mock(),
        Mock(),
        "value",
        Mock(),
        Mock(),
        Mock(),
    )
    return concept


@pytest.fixture
def temperature_space(temperature_concept):
    space = ConceptualSpace(
        "",
        "",
        "temperature",
        temperature_concept,
        [],
        StructureCollection(),
        1,
        [],
        [],
        is_basic_level=True,
    )
    return space


@pytest.fixture
def mild_concept(temperature_space):
    concept = Concept(
        "",
        "",
        "mild",
        Location([[10]], temperature_space),
        ProximityClassifier(),
        "value",
        Mock(),
        Mock(),
        distance_function=centroid_euclidean_distance,
    )
    temperature_space.add(concept)
    return concept


@pytest.fixture
def input_concept():
    concept = Concept(
        "",
        "",
        "input",
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    return concept


@pytest.fixture
def input_space(input_concept):
    space = WorkingSpace(
        "",
        "",
        "input",
        input_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def interpretation_concept():
    concept = Concept(
        "",
        "",
        "interpretation",
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    return concept


@pytest.fixture
def interpretation_space(interpretation_concept):
    space = WorkingSpace(
        "",
        "",
        "interpretation",
        interpretation_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def interpretation_temperature_space(interpretation_space, temperature_space):
    return temperature_space.instance_in_space(interpretation_space)


@pytest.fixture
def target_view(bubble_chamber, input_space, interpretation_space):
    view = MonitoringView(
        "",
        "",
        Mock(),
        Mock(),
        StructureCollection({input_space, interpretation_space}),
        Mock(),
        Mock(),
    )
    bubble_chamber.views.add(view)
    return view


@pytest.fixture
def target_interpretation_chunk(
    interpretation_space, interpretation_temperature_space, mild_concept
):
    chunk = Chunk(
        "",
        "",
        Mock(),
        [
            Location([], interpretation_space),
            Location([[10]], interpretation_temperature_space),
        ],
        StructureCollection(),
        interpretation_space,
        Mock(),
    )
    interpretation_space.add(chunk)
    interpretation_temperature_space.add(chunk)
    label = Label("", "", chunk, mild_concept, interpretation_temperature_space, 1)
    chunk.links_out.add(label)
    interpretation_temperature_space.add(label)
    return chunk


@pytest.fixture
def target_raw_chunk(input_space):
    chunk = Chunk(
        "",
        "",
        [[10]],
        [Location([[0, 0]], input_space)],
        StructureCollection(),
        input_space,
        Mock(),
        is_raw=True,
    )
    input_space.add(chunk)
    return chunk


def test_successful_projects_raw_chunk_and_same_chunk_cannot_be_projected_again(
    bubble_chamber, target_view, target_interpretation_chunk, target_raw_chunk
):
    builder = ReverseChunkProjectionBuilder.spawn(
        "",
        bubble_chamber,
        target_view,
        target_interpretation_chunk,
        target_raw_chunk,
        1.0,
    )
    assert not target_raw_chunk.has_correspondence_to_space(
        target_view.interpretation_space
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert hasinstance(builder.child_structures, Chunk)
    assert target_raw_chunk.has_correspondence_to_space(
        target_view.interpretation_space
    )
    builder = ReverseChunkProjectionBuilder.spawn(
        "",
        bubble_chamber,
        target_view,
        target_interpretation_chunk,
        target_raw_chunk,
        1.0,
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
