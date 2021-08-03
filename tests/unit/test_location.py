import pytest
from unittest.mock import Mock

from homer.location import Location
from homer.tools import centroid_euclidean_distance


@pytest.mark.parametrize(
    "sets_of_coordinates, expected_coordinates",
    [
        ([[1, 1, 1], [3, 3, 3]], [2, 2, 2]),
        ([[1, 1, 1, 1], [3, 3, 3, 3]], [2, 2, 2, 2]),
        ([[1, 1], [2, 2]], [1.5, 1.5]),
    ],
)
def test_average(sets_of_coordinates, expected_coordinates):
    locations = [
        Location([sets_of_coordinates[i]], Mock())
        for i in range(len(sets_of_coordinates))
    ]
    average = Location.average(locations)
    assert [expected_coordinates] == average.coordinates


@pytest.mark.parametrize(
    "coordinates_one, coordinates_two, expected_coordinates",
    [
        ([[0]], [[1]], [[0], [1]]),
        ([[0], [1]], [[2], [4]], [[0], [4]]),
    ],
)
def test_merge(coordinates_one, coordinates_two, expected_coordinates):
    space = Mock()
    location_one = Location(coordinates_one, space)
    location_two = Location(coordinates_two, space)
    merged_location = Location.merge(location_one, location_two)
    assert expected_coordinates == merged_location.coordinates


@pytest.mark.parametrize(
    "coordinates_one, coordinates_two",
    [([[0], [1]], [[3], [4]]), ([[3], [4]], [[0], [1]])],
)
def test_will_not_merge_non_adjacent_locations(coordinates_one, coordinates_two):
    space = Mock()
    location_one = Location(coordinates_one, space)
    location_two = Location(coordinates_two, space)
    with pytest.raises(Exception):
        Location.merge(location_one, location_two)


@pytest.mark.parametrize(
    "self_coordinates, other_coordinates, expected",
    [([1, 1], [1, 1], True), ([1, 1], [1, 2], False)],
)
def test_eq(self_coordinates, other_coordinates, expected):
    space = Mock()
    location_1 = Location(self_coordinates, space)
    location_2 = Location(other_coordinates, space)
    assert expected == (location_1 == location_2)


@pytest.mark.parametrize(
    "self_coordinates, other_coordinates, nearness, expected",
    [
        ([[1, 1]], [[1, 1]], 0, True),
        ([[1, 2]], [[1, 1]], 0, False),
        ([[1, 2]], [[1, 1]], 1, True),
    ],
)
def test_is_near(self_coordinates, other_coordinates, nearness, expected):
    space = Mock()
    space.parent_concept.distance_to_proximity_weight = nearness
    space.parent_concept.distance_function = centroid_euclidean_distance
    location_1 = Location(self_coordinates, space)
    location_2 = Location(other_coordinates, space)
    assert expected == location_1.is_near(location_2)
