import math
import pytest
from unittest.mock import Mock, patch

from homer.perceptlet import Perceptlet
from homer.perceptlets.correspondence import Correspondence
from homer.perceptlet_collection import PerceptletCollection


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
    perceptlet = Perceptlet("value", Mock(), set(), Mock())
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
    perceptlet = Perceptlet("value", Mock(), set(), Mock())
    for label_strength in label_strengths:
        label = Mock()
        label.strength = label_strength
        perceptlet.labels.add(label)
    actual_importance = perceptlet._label_based_importance
    assert math.isclose(
        expected_importance, actual_importance, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


@pytest.mark.parametrize(
    "number_of_connections, expected_unhappiness",
    [(0, 1.0), (1, 1.0), (3, 0.333), (5, 0.2)],
)
def test_unhappiness_based_on_connections(number_of_connections, expected_unhappiness):
    perceptlet = Perceptlet("value", Mock(), set(), Mock())
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
    valid_neighbour = Perceptlet("value", Mock(), set(), Mock())
    valid_neighbour.labels.add(label)
    invalid_neighbour = Perceptlet("value", Mock(), set(), Mock())
    valid_neighbours = [valid_neighbour for i in range(no_of_valid_neighbours)]
    invalid_neighbours = [invalid_neighbour for i in range(no_of_invalid_neighbours)]
    neighbours = valid_neighbours + invalid_neighbours
    perceptlet = Perceptlet("value", Mock(), neighbours, Mock())
    assert no_of_valid_neighbours == perceptlet.number_of_neighbours_with_label(concept)
    actual_proportion = perceptlet.proportion_of_neighbours_with_label(concept)
    assert math.isclose(
        expected_proportion, actual_proportion, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


def test_has_label(concept, label):
    perceptlet = Perceptlet("value", Mock(), set(), Mock())
    perceptlet.labels.add(label)
    assert perceptlet.has_label(concept)


def test_labels_in_space(space, label):
    perceptlet = Perceptlet("value", Mock(), set(), Mock())
    perceptlet.labels.add(label)
    assert {label} == perceptlet.labels_in_space(space).perceptlets


def test_has_label_in_space(space, label):
    perceptlet = Perceptlet("value", Mock(), set(), Mock())
    perceptlet.labels.add(label)
    assert perceptlet.has_label_in_space(space)


def test_makes_group_with():
    member_1 = Perceptlet("value", Mock(), set(), Mock())
    member_2 = Mock()
    member_3 = Mock()
    other_members = PerceptletCollection({member_2, member_3})
    group = Mock()
    group.members = PerceptletCollection({member_1, member_2, member_3})
    member_1.groups.add(group)
    assert member_1.makes_group_with(other_members)


@pytest.mark.parametrize(
    "is_between, is_in_space, expected",
    [
        (True, True, True),
        (True, False, False),
        (False, True, False),
        (False, False, False),
    ],
)
def test_has_correspondence(is_between, is_in_space, expected):
    second_perceptlet = Mock()
    space = Mock()
    with patch.object(Correspondence, "is_between", return_value=is_between):
        correspondence = Correspondence(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
        if is_in_space:
            correspondence.parent_concept = space
        perceptlet = Perceptlet("value", Mock(), set(), Mock())
        perceptlet.correspondences = {correspondence}
        assert expected == perceptlet.has_correspondence(second_perceptlet, space)
