import pytest

from homer.tools import *


@pytest.mark.parametrize(
    "vectors, expected_average",
    [([[1, 1, 1], [2, 2, 2], [3, 3, 3]], [2, 2, 2]), ([[1], [2]], [1.5])],
)
def test_average_vector(vectors, expected_average):
    assert average_vector(vectors) == expected_average
