import pytest
from unittest.mock import Mock

from homer.codelets import Evaluator, Publisher, Suggester
from homer.codelets.factories import RandomFactory
from homer.structure_collection import StructureCollection


def test_decide_follow_up_class_returns_codelet_class(bubble_chamber):
    coderack = Mock()
    factory_codelet = RandomFactory(Mock(), Mock(), bubble_chamber, coderack, Mock())
    follow_up_class = factory_codelet._decide_follow_up_class()
    codelet_types = [Suggester, Evaluator, Publisher]
    assert (
        follow_up_class in codelet_types
        or follow_up_class.__bases__[0] in codelet_types
        or follow_up_class.__bases__[0].__bases__[0] in codelet_types
    )
