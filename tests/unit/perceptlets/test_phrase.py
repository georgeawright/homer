import math
import pytest
from unittest.mock import Mock

from homer.perceptlets.phrase import Phrase

FLOAT_COMPARISON_TOLERANCE = 1e-3


@pytest.mark.parametrize(
    "word_importances, expected_importance",
    [([0.0, 0.0], 0.0), ([1.0, 1.0], 1.0), ([1.0, 0], 1.0), ([0.0, 0.5], 0.5)],
)
def test_importance(word_importances, expected_importance):
    words = []
    for importance in word_importances:
        word = Mock()
        word.importance = importance
        words.append(word)
    phrase = Phrase("value", words, Mock(), Mock())
    assert expected_importance == phrase.importance


@pytest.mark.parametrize(
    "number_of_relations, expected_unhappiness",
    [(0, 1.0), (1, 1.0), (3, 0.333), (5, 0.2)],
)
def test_unhappiness(number_of_relations, expected_unhappiness):
    phrase = Phrase("value", Mock(), Mock(), Mock())
    for i in range(number_of_relations):
        phrase.add_relation(Mock())
    assert math.isclose(
        expected_unhappiness, phrase.unhappiness, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )
