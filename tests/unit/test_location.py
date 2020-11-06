import pytest
from unittest.mock import Mock

from homer.location import Location


@pytest.mark.parametrize(
    "xs, ys, expected_x, expected_y",
    [([1, 2, 3], [4, 5, 6], 2, 5), ([1, 2, 3, 4], [4, 5, 6, 7], 2.5, 5.5)],
)
def test_average(xs, ys, expected_x, expected_y):
    locations = [Location(xs[i], ys[i], Mock()) for i in range(len(xs))]
    average = Location.average(locations)
    assert expected_x == average.x
    assert expected_y == average.y
