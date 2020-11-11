import math
import pytest
from unittest.mock import Mock

from homer.structures import Concept


@pytest.fixture
def structure():
    s = Mock()
    s.coordinates = [1, 2]
    s.latitude = [1]
    s.longitude = [2]
    s.value = [10]
    return s


@pytest.mark.parametrize(
    "prototype, relevant_value, distance_function, expected",
    [
        ([10], "value", math.dist, 0),
        ([9], "value", math.dist, 1),
        ([3], "latitude", math.dist, 2),
        ([2, 2], "coordinates", math.dist, 1),
    ],
)
def test_distance_from(
    prototype, relevant_value, distance_function, expected, structure
):
    concept = Concept(
        Mock(), prototype, Mock(), Mock(), relevant_value, Mock(), distance_function
    )
    assert expected == concept.distance_from(structure)


@pytest.mark.parametrize(
    "prototype, relevant_value, distance_function, distance_to_proximity_weight, expected",
    [
        ([10], "value", math.dist, 1.5, 1),
        ([9], "value", math.dist, 1.5, 1),
        ([3], "latitude", math.dist, 1.5, 0.75),
        ([2, 2], "coordinates", math.dist, 1.5, 1),
    ],
)
def test_proximity_to(
    prototype,
    relevant_value,
    distance_function,
    distance_to_proximity_weight,
    expected,
    structure,
):
    concept = Concept(
        Mock(), prototype, Mock(), Mock(), relevant_value, Mock(), distance_function
    )
    concept.DISTANCE_TO_PROXIMITY_WEIGHT = distance_to_proximity_weight
    assert expected == concept.proximity_to(structure)
