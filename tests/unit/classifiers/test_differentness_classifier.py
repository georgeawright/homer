import pytest
from unittest.mock import Mock

from homer.classifiers import DifferentnessClassifier


def test_classifies_slots_as_not_different():
    start_slot = Mock()
    start_slot.is_slot = True
    end_slot = Mock()
    end_slot.is_slot = True
    start_non_slot = Mock()
    start_non_slot.is_slot = False
    end_non_slot = Mock()
    end_non_slot.is_slot = False
    classifier = DifferentnessClassifier()
    assert 0 == classifier.classify_link(start=start_slot, end=end_slot)
    assert 0 == classifier.classify_link(start=start_non_slot, end=end_slot)
    assert 0 == classifier.classify_link(start=start_slot, end=end_non_slot)
