from unittest.mock import Mock

from homer.structures import Link


def test_spread_activation():
    parent_concept = Mock()
    link = Link(Mock(), Mock(), parent_concept, Mock(), Mock())
    link._activation = 1.0
    link.spread_activation()
    parent_concept.boost_activation.assert_called()
