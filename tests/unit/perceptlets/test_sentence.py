import math
import pytest
from unittest.mock import Mock

from homer.perceptlets.sentence import Sentence


FLOAT_COMPARISON_TOLERANCE = 1e-3


@pytest.mark.parametrize("phrase_sizes, expected_size", [([1, 2, 3], 6), ([10], 10)])
def test_size(phrase_sizes, expected_size):
    phrases = []
    for size in phrase_sizes:
        phrase = Mock()
        phrase.size = size
        phrases.append(phrase)
    sentence = Sentence("text", phrases, Mock(), Mock())
    assert expected_size == sentence.size


@pytest.mark.parametrize(
    "sentence_size, expected_importance", [(1, 0), (2, 0.5), (10, 0.9), (100, 0.99)]
)
def test_size_based_importance(sentence_size, expected_importance):
    phrase = Mock()
    phrase.size = sentence_size
    sentence = Sentence("text", [phrase], Mock(), Mock())
    assert math.isclose(
        expected_importance,
        sentence._size_based_importance,
        abs_tol=FLOAT_COMPARISON_TOLERANCE,
    )


@pytest.mark.parametrize(
    "number_of_labels, number_of_relations, expected_unhappiness",
    [(0, 0, 1.0), (1, 0, 1.0), (1, 1, 0.5), (2, 3, 0.2)],
)
def test_unhappiness(number_of_labels, number_of_relations, expected_unhappiness):
    sentence = Sentence("value", Mock(), Mock(), Mock())
    for i in range(number_of_labels):
        sentence.add_label(Mock())
    for i in range(number_of_relations):
        sentence.add_relation(Mock())
    assert math.isclose(
        expected_unhappiness, sentence.unhappiness, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )
