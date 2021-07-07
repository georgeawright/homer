import math
import pytest
from unittest.mock import Mock

from homer.structures.nodes import Concept
from homer.tools import centroid_euclidean_distance


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
        parent_space,
        Mock(),
        distance_function,
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
        parent_space,
        Mock(),
        distance_function,
        distance_to_proximity_weight=distance_to_proximity_weight,
    )
    assert expected == concept.proximity_to(structure)
