from unittest.mock import Mock

from homer.worldview import Worldview


def test_add_perceptlet():
    worldview = Worldview(set())
    assert set() == worldview.perceptlets
    perceptlet = Mock()
    worldview.add_perceptlet(perceptlet)
    assert {perceptlet} == worldview.perceptlets


def test_remove_perceptlet():
    perceptlet = Mock()
    worldview = Worldview({perceptlet})
    assert {perceptlet} == worldview.perceptlets
    worldview.remove_perceptlet(perceptlet)
    assert set() == worldview.perceptlets
