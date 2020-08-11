import math
import pytest
from unittest.mock import Mock

from homer.perceptlets.textlet import Textlet


FLOAT_COMPARISON_TOLERANCE = 1e-3


def test_size_flat_textlet():
    expected_size = 30
    constituents = []
    for _ in range(expected_size):
        constituent = Mock()
        constituent.size = 1
        constituents.append(constituent)
    textlet = Textlet("text", constituents, Mock(), Mock(), Mock())
    assert expected_size == textlet.size


def test_size_recursive_textlet():
    textlet_depth = 30
    base_constituent = Mock()
    base_constituent.size = 1
    constituents = [base_constituent]
    for _ in range(textlet_depth):
        constituents = [Textlet("text", constituents, Mock(), Mock(), Mock())]
    textlet = Textlet("text", constituents, Mock(), Mock(), Mock())
    assert 1 == textlet.size


@pytest.mark.parametrize(
    "textlet_size, expected_importance", [(1, 0), (2, 0.5), (10, 0.9), (100, 0.99)]
)
def test_size_based_importance(textlet_size, expected_importance):
    constituent = Mock()
    constituent.size = textlet_size
    textlet = Textlet("text", [constituent], Mock(), Mock(), Mock())
    assert math.isclose(
        expected_importance,
        textlet._size_based_importance,
        abs_tol=FLOAT_COMPARISON_TOLERANCE,
    )


@pytest.mark.parametrize(
    "number_of_labels, number_of_relations, expected_unhappiness",
    [(0, 0, 1.0), (1, 0, 1.0), (1, 1, 0.5), (2, 3, 0.2)],
)
def test_unhappiness(number_of_labels, number_of_relations, expected_unhappiness):
    textlet = Textlet("value", Mock(), Mock(), Mock(), Mock())
    for i in range(number_of_labels):
        textlet.add_label(Mock())
    for i in range(number_of_relations):
        textlet.add_relation(Mock())
    assert math.isclose(
        expected_unhappiness, textlet.unhappiness, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )
