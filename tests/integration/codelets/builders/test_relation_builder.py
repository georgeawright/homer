import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import DifferenceClassifier, ProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.builders import RelationBuilder
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.links import Relation
from homer.structures.spaces import ConceptualSpace, WorkingSpace


@pytest.fixture
def relational_concepts_space():
    space = ConceptualSpace(
        "relational concepts", StructureCollection({more_concept}), Mock()
    )
    return space


@pytest.fixture
def more_less_concept(relational_concepts_space):
    return Concept.new(
        "more-less",
        None,
        None,
        relational_concepts_space,
        "value",
        StructureCollection(),
        math.dist,
    )


@pytest.fixture
def more_less_space(more_less_concept):
    space = ConceptualSpace("more-less", StructureCollection(), more_less_concept)
    more_less_concept.child_spaces.add(space)
    return space


@pytest.fixture
def more_concept(more_less_space):
    classifier = DifferenceClassifier(ProximityClassifier())
    more = Concept(
        "more",
        [5],
        classifier,
        more_less_space,
        "value",
        StructureCollection(),
        math.dist,
    )
    more_less_space.contents.add(more)
    return more


@pytest.fixture
def target_space():
    temperature = Concept(
        "temperature",
        None,
        Mock(),
        Mock(),
        "value",
        StructureCollection(),
        math.dist,
    )
    temperature_space = ConceptualSpace(
        "temperature", StructureCollection(), temperature
    )
    return temperature_space


@pytest.fixture
def bubble_chamber(more_concept, relational_concepts_space):
    chamber = BubbleChamber(
        Mock(),
        Mock(),
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
    chamber.concepts.add(more_concept)
    chamber.spaces.add(relational_concepts_space)
    return chamber


@pytest.fixture
def target_chunk(bubble_chamber, target_space):
    location_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    input_space = WorkingSpace("input", StructureCollection(), 0, location_concept)
    parent_spaces = StructureCollection({input_space})
    chunk = Chunk(
        [10],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    second_chunk = Chunk(
        [5],
        Location([0, 1], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    chunk.neighbours.add(second_chunk)
    bubble_chamber.chunks.add(chunk)
    bubble_chamber.chunks.add(second_chunk)
    input_space.contents.add(chunk)
    input_space.contents.add(second_chunk)
    target_space.contents.add(chunk)
    target_space.contents.add(second_chunk)
    chunk.parent_spaces.add(input_space)
    second_chunk.parent_spaces.add(input_space)
    chunk.parent_spaces.add(target_space)
    second_chunk.parent_spaces.add(target_space)
    return chunk


def test_successful_adds_relation_to_chunk_and_spawns_follow_up_and_same_relation_cannot_be_recreated(
    bubble_chamber, target_space, target_chunk
):
    parent_id = ""
    urgency = 1.0

    builder = RelationBuilder.spawn(
        parent_id, bubble_chamber, target_space, target_chunk, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Relation)
    assert isinstance(builder.child_codelets[0], RelationBuilder)
    builder = RelationBuilder.spawn(
        parent_id, bubble_chamber, target_space, target_chunk, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
