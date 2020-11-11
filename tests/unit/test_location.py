import pytest
from unittest.mock import Mock

from homer.location import Location


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
        Location(sets_of_coordinates[i], Mock())
        for i in range(len(sets_of_coordinates))
    ]
    average = Location.average(locations)
    assert expected_coordinates == average.coordinates


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
    [([1, 1], [1, 1], 0, True), ([1, 2], [1, 1], 0, False), ([1, 2], [1, 1], 1, True)],
)
def test_is_near(self_coordinates, other_coordinates, nearness, expected):
    Location.NEARNESS = nearness
    space = Mock()
    location_1 = Location(self_coordinates, space)
    location_2 = Location(other_coordinates, space)
    assert expected == location_1.is_near(location_2)
