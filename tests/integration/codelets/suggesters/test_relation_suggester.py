import pytest
from unittest.mock import Mock
from typing import List

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import DifferenceClassifier, ProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.builders import RelationBuilder
from homer.codelets.suggesters import RelationSuggester
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Chunk, Concept
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.tools import centroid_euclidean_distance, hasinstance


@pytest.fixture
def relational_concepts_space():
    space = ConceptualSpace(
        "relational concepts",
        Mock(),
        "relational concepts",
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    return space


@pytest.fixture
def more_less_concept(relational_concepts_space):
    concept = Concept(
        Mock(),
        Mock(),
        "more-less",
        [Location(Mock(), relational_concepts_space)],
        Mock(),
        list,
        Mock(),
        StructureCollection(),
        centroid_euclidean_distance,
    )
    relational_concepts_space.contents.add(concept)
    return concept


@pytest.fixture
def more_less_space(relational_concepts_space, more_less_concept):
    space = ConceptualSpace(
        "more-less",
        Mock(),
        "more-less",
        more_less_concept,
        [Location([], relational_concepts_space)],
        StructureCollection(),
        1,
        [],
        [],
    )
    relational_concepts_space.add(space)
    more_less_concept.child_spaces.add(space)
    return space


@pytest.fixture
def more_concept(more_less_space):
    classifier = DifferenceClassifier(ProximityClassifier())
    more = Concept(
        Mock(),
        Mock(),
        "more",
        [Location([[5]], more_less_space)],
        classifier,
        Mock(),
        more_less_space,
        StructureCollection(),
        centroid_euclidean_distance,
    )
    more_less_space.contents.add(more)
    return more


@pytest.fixture
def temperature_space():
    temperature = Concept(
        Mock(),
        Mock(),
        "temperature",
        Mock(),
        Mock(),
        list,
        Mock(),
        StructureCollection(),
        centroid_euclidean_distance,
    )
    temperature_space = ConceptualSpace(
        Mock(), Mock(), "temperature", temperature, [], StructureCollection(), 1, [], []
    )
    return temperature_space


@pytest.fixture
def bubble_chamber(more_concept, relational_concepts_space):
    chamber = BubbleChamber.setup(Mock())
    chamber.concepts.add(more_concept)
    chamber.conceptual_spaces.add(relational_concepts_space)
    relation_concept = Concept(
        Mock(),
        Mock(),
        "relation",
        Mock(),
        Mock(),
        "value",
        Mock(),
        StructureCollection(),
        Mock(),
    )
    chamber.concepts.add(relation_concept)
    suggest_concept = Concept(
        Mock(),
        Mock(),
        "suggest",
        Mock(),
        Mock(),
        "value",
        Mock(),
        StructureCollection(),
        Mock(),
    )
    chamber.concepts.add(suggest_concept)
    relation = Relation(
        Mock(), Mock(), relation_concept, suggest_concept, None, None, 1
    )
    relation_concept.links_out.add(relation)
    suggest_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def target_chunk(bubble_chamber, temperature_space):
    location_concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        "coordinates",
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    input_space = WorkingSpace(
        Mock(),
        Mock(),
        "input",
        location_concept,
        Mock(),
        [],
        StructureCollection(),
        0,
        [],
        [],
    )
    chunk = Chunk(
        Mock(),
        Mock(),
        [Location([[0, 0]], input_space), Location([[10]], temperature_space)],
        StructureCollection(),
        Mock(),
        0.0,
    )
    second_chunk = Chunk(
        Mock(),
        Mock(),
        [Location([[0, 1]], input_space), Location([[5]], temperature_space)],
        StructureCollection(),
        Mock(),
        0.0,
    )
    bubble_chamber.chunks.add(chunk)
    bubble_chamber.chunks.add(second_chunk)
    input_space.contents.add(chunk)
    input_space.contents.add(second_chunk)
    temperature_space.contents.add(chunk)
    temperature_space.contents.add(second_chunk)
    chunk.parent_spaces.add(input_space)
    second_chunk.parent_spaces.add(input_space)
    chunk.parent_spaces.add(temperature_space)
    second_chunk.parent_spaces.add(temperature_space)
    return chunk


@pytest.mark.skip
def test_gives_high_confidence_for_compatible_chunks_and_spawns_follow_up(
    bubble_chamber, temperature_space, target_chunk
):
    parent_id = ""
    urgency = 1.0

    suggester = RelationSuggester.spawn(
        parent_id,
        bubble_chamber,
        {
            "target_structure_one": target_chunk,
            "target_structure_two": None,
            "target_space": temperature_space,
            "parent_concept": None,
        },
        urgency,
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert isinstance(suggester.child_codelets[0], RelationBuilder)
