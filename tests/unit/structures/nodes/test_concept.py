import pytest
from unittest.mock import Mock

from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.nodes import Concept
from linguoplotter.tools import centroid_euclidean_distance


def test_letter_chunk_forms(bubble_chamber):
    hot_concept = Concept(
        Mock(),
        Mock(),
        "hot",
        [],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    hot_word = Mock()
    hot_word.name = "hot"
    hott_word = Mock()
    hott_word.name = "hott"

    jj_concept = Mock()
    jjr_concept = Mock()

    jj_link = Mock()
    jj_link.parent_concept = jj_concept
    jj_link.arguments = StructureCollection(Mock(), [hot_concept, hot_word])
    hot_concept.links_out.add(jj_link)

    jjr_link = Mock()
    jjr_link.parent_concept = jjr_concept
    jjr_link.arguments = StructureCollection(Mock(), [hot_concept, hott_word])
    hot_concept.links_out.add(jjr_link)

    assert hot_concept.letter_chunk_forms() == StructureCollection(
        Mock(), [hot_word, hott_word]
    )
    assert hot_concept.letter_chunk_forms(jj_concept) == StructureCollection(
        Mock(), [hot_word]
    )
    assert hot_concept.letter_chunk_forms(jjr_concept) == StructureCollection(
        Mock(), [hott_word]
    )


@pytest.fixture
def structure():
    temperature_location = Mock()
    temperature_location.coordinates = [[10]]
    location_location = Mock()
    location_location.coordinates = [[1, 2]]
    s = Mock()
    s.location_in_space = lambda space: {
        "temperature": temperature_location,
        "location": location_location,
    }[space.name]
    s.location_in_conceptual_space = lambda space: {
        "temperature": temperature_location,
        "location": location_location,
    }[space.name]
    return s


@pytest.mark.parametrize(
    "prototype, space_name, distance_function, expected",
    [
        ([[10]], "temperature", centroid_euclidean_distance, 0),
        ([[9]], "temperature", centroid_euclidean_distance, 1),
        ([[2, 2]], "location", centroid_euclidean_distance, 1),
    ],
)
def test_distance_from(prototype, space_name, distance_function, expected, structure):
    parent_space = Mock()
    parent_space.name = space_name
    location = Mock()
    location.space = parent_space
    location.coordinates = prototype
    concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        [location],
        Mock(),
        Mock(),
        Mock(),
        parent_space,
        Mock(),
        distance_function,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert expected == concept.distance_from(structure)


@pytest.mark.parametrize(
    "prototype, space_name, distance_function, distance_to_proximity_weight, expected",
    [
        ([[10]], "temperature", centroid_euclidean_distance, 1.5, 1),
        ([[9]], "temperature", centroid_euclidean_distance, 1.5, 1),
        ([[2, 2]], "location", centroid_euclidean_distance, 1.5, 1),
    ],
)
def test_proximity_to(
    prototype,
    space_name,
    distance_function,
    distance_to_proximity_weight,
    expected,
    structure,
):
    parent_space = Mock()
    parent_space.name = space_name
    location = Mock()
    location.space = parent_space
    location.coordinates = prototype
    concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        [location],
        Mock(),
        Mock(),
        Mock(),
        parent_space,
        Mock(),
        distance_function,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        distance_to_proximity_weight=distance_to_proximity_weight,
    )
    assert expected == concept.proximity_to(structure)
