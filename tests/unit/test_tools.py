import pytest

from homer.tools import *


@pytest.mark.parametrize(
    "vectors, expected_average",
    [([[1, 1, 1], [2, 2, 2], [3, 3, 3]], [2, 2, 2]), ([[1], [2]], [1.5])],
)
def test_average_vector(vectors, expected_average):
    assert average_vector(vectors) == expected_average


def test_has_instance():
    list_with_int = [1, "a", "b"]
    assert hasinstance(list_with_int, int)
    list_without_int = ["1", "a", "b"]
    assert not hasinstance(list_without_int, int)


def test_are_instances():
    list_of_ints = [1, 2, 3]
    assert areinstances(list_of_ints, int)
    assert not areinstances(list_of_ints, str)
