from unittest.mock import Mock

from homer.bubbles.perceptlets import Textlet


def test_size_flat_textlet():
    expected_size = 30
    constituents = []
    for _ in range(expected_size):
        constituent = Mock()
        constituent.size = 1
        constituents.append(constituent)
    textlet = Textlet(Mock(), Mock(), Mock(), constituents, Mock(), Mock(), Mock())
    assert expected_size == textlet.size


def test_size_recursive_textlet():
    textlet_depth = 30
    base_constituent = Mock()
    base_constituent.size = 1
    constituents = [base_constituent]
    for _ in range(textlet_depth):
        constituents = [
            Textlet(Mock(), Mock(), Mock(), constituents, Mock(), Mock(), Mock())
        ]
    textlet = Textlet(Mock(), Mock(), Mock(), constituents, Mock(), Mock(), Mock())
    assert 1 == textlet.size
