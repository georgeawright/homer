import math
import pytest
from unittest.mock import Mock

from homer.perceptlet import Perceptlet


FLOAT_COMPARISON_TOLERANCE = 1e-3


@pytest.fixture
def space():
    mock_concept = Mock()
    return mock_concept


@pytest.fixture
def concept(space):
    mock_concept = Mock()
    mock_concept.space = space
    return mock_concept


@pytest.fixture
def label(concept):
    mock_label = Mock()
    mock_label.parent_concept = concept
    return mock_label


def test_exigency_raises_not_implemented_error():
    perceptlet = Perceptlet("value", set())
    with pytest.raises(NotImplementedError):
        perceptlet.exigency


@pytest.mark.parametrize(
    "label_strengths, expected_importance",
    [
        ([], 0),
        ([0.2, 0.3], 0.333),
        ([0.7, 0.8], 0.6),
        ([1, 1], 0.667),
        ([1, 1, 1, 1], 0.8),
    ],
)
def test_label_based_importance(label_strengths, expected_importance):
    perceptlet = Perceptlet("value", set())
    for label_strength in label_strengths:
        label = Mock()
        label.strength = label_strength
        perceptlet.add_label(label)
    actual_importance = perceptlet._label_based_importance
    assert math.isclose(
        expected_importance, actual_importance, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


@pytest.mark.parametrize(
    "number_of_connections, expected_unhappiness",
    [(0, 1.0), (1, 1.0), (3, 0.333), (5, 0.2)],
)
def test_unhappiness_based_on_connections(number_of_connections, expected_unhappiness):
    perceptlet = Perceptlet("value", set())
    connections = {Mock() for _ in range(number_of_connections)}
    actual_unhappiness = perceptlet._unhappiness_based_on_connections(connections)
    assert math.isclose(
        expected_unhappiness, actual_unhappiness, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


@pytest.mark.parametrize(
    "no_of_valid_neighbours, no_of_invalid_neighbours, expected_proportion",
    [(1, 1, 0.5), (1, 2, 0.33333), (0, 1, 0.0)],
)
def test_number_and_proportion_of_neighbours_with_label(
    concept,
    label,
    no_of_valid_neighbours,
    no_of_invalid_neighbours,
    expected_proportion,
):
    valid_neighbour = Perceptlet("value", set())
    valid_neighbour.labels.add(label)
    invalid_neighbour = Perceptlet("value", set())
    valid_neighbours = [valid_neighbour for i in range(no_of_valid_neighbours)]
    invalid_neighbours = [invalid_neighbour for i in range(no_of_invalid_neighbours)]
    neighbours = valid_neighbours + invalid_neighbours
    print(neighbours)
    perceptlet = Perceptlet("value", neighbours)
    assert no_of_valid_neighbours == perceptlet.number_of_neighbours_with_label(concept)
    actual_proportion = perceptlet.proportion_of_neighbours_with_label(concept)
    assert math.isclose(
        expected_proportion, actual_proportion, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


def test_get_random_neighbour():
    perceptlet = Perceptlet("value", [Mock(), Mock(), Mock()])
    assert perceptlet.get_random_neighbour() in perceptlet.neighbours


def test_has_label(concept, label):
    perceptlet = Perceptlet("value", set())
    perceptlet.labels.add(label)
    assert perceptlet.has_label(concept)


def test_labels_in_space(space, label):
    perceptlet = Perceptlet("value", set())
    perceptlet.labels.add(label)
    assert {label} == perceptlet.labels_in_space(space)


def has_label_in_space(space, label):
    perceptlet = Perceptlet("value", set())
    perceptlet.labels.add(label)
    assert perceptlet.has_label_in_space(space)


def test_add_label(label):
    perceptlet = Perceptlet("value", set())
    assert set() == perceptlet.labels
    perceptlet.add_label(label)
    assert {label} == perceptlet.labels


def test_add_neighbour():
    perceptlet = Perceptlet("value", set())
    assert set() == perceptlet.neighbours
    neighbour = Mock()
    perceptlet.add_neighbour(neighbour)
    assert {neighbour} == perceptlet.neighbours


def test_remove_neighbour():
    neighbour = Mock()
    perceptlet = Perceptlet("value", {neighbour})
    assert {neighbour} == perceptlet.neighbours
    perceptlet.remove_neighbour(neighbour)
    assert set() == perceptlet.neighbours
