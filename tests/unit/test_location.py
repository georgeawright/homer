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
