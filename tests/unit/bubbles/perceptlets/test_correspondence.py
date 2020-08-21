from unittest.mock import Mock

from homer.bubbles.perceptlets import Correspondence


def test_is_between():
    first = Mock()
    second = Mock()
    third = Mock()
    correspondence = Correspondence(Mock(), Mock(), first, second, Mock(), Mock())
    assert correspondence.is_between(first, second)
    assert correspondence.is_between(second, first)
    assert not correspondence.is_between(first, third)
    assert not correspondence.is_between(third, second)
