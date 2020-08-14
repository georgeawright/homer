import pytest
from unittest.mock import Mock

from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet
from homer.perceptlet_collection import PerceptletCollection
from homer.workspace_location import WorkspaceLocation


def setup_module(module):
    HyperParameters.ACTIVATION_PATTERN_DEPTH = 1
    HyperParameters.ACTIVATION_PATTERN_HEIGHT = 3
    HyperParameters.ACTIVATION_PATTERN_WIDTH = 3
    HyperParameters.WORKSPACE_DEPTH = 1
    HyperParameters.WORKSPACE_HEIGHT = 6
    HyperParameters.WORKSPACE_WIDTH = 5


@pytest.fixture
def perceptlet():
    perceptlet = Mock()
    perceptlet.location = [0, 0, 0]
    return perceptlet


def test_iterate(perceptlet):
    collection = PerceptletCollection({perceptlet})
    for perceptlet in collection:
        assert True


def test_at(perceptlet):
    collection = PerceptletCollection({perceptlet})
    location = WorkspaceLocation(0, 0, 0)
    assert {perceptlet} == collection.at(location).perceptlets


def test_add():
    perceptlet = Perceptlet(Mock(), [0, 0, 0], Mock(), Mock())
    collection = PerceptletCollection(set())
    collection._arrange_perceptlets_by_location()
    collection.add(perceptlet)
    assert {perceptlet} == collection.perceptlets
    assert [
        [[{perceptlet}, set(), set()], [set(), set(), set()], [set(), set(), set()]]
    ] == collection.perceptlets_by_location


def test_remove(perceptlet):
    collection = PerceptletCollection({perceptlet})
    collection._arrange_perceptlets_by_location()
    collection.remove(perceptlet)
    assert set() == collection.perceptlets
    assert [
        [[set(), set(), set()], [set(), set(), set()], [set(), set(), set()]]
    ] == collection.perceptlets_by_location
