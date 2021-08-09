import pytest
from unittest.mock import Mock

from homer.classifiers import ProximityClassifier


@pytest.mark.parametrize("proximity", [(1.0), (0.0)])
def test_classify_link(proximity):
    classifier = ProximityClassifier()
    concept = Mock()
    concept.proximity_to.return_value = proximity
    example = Mock()
    assert proximity == classifier.classify_link(concept=concept, start=example)


def test_classify_chunk_with_no_root():
    classifier = ProximityClassifier()
    root = None
    child = Mock()
    assert 1.0 == classifier.classify_chunk(root=root, child=child)


@pytest.mark.parametrize("member_proximity", [(0.0), (0.5), (1.0)])
def test_classify_chunk_with_no_child(member_proximity):
    classifier = ProximityClassifier()
    root = Mock()
    child = None
    root_member = Mock()
    root_member.is_slot = False
    parent_space = Mock()
    parent_space.is_conceptual_space = True
    parent_space.is_basic_level = True
    parent_space.proximity_between.return_value = member_proximity
    root.parent_spaces = [parent_space]
    root.members = [root_member]
    assert member_proximity == classifier.classify_chunk(root=root, child=child)


@pytest.mark.parametrize("child_proximity", [(0.0), (0.5), (1.0)])
def test_classfiy_chunk_with_root_and_child(child_proximity):
    classifier = ProximityClassifier()
    root = Mock()
    child = Mock()
    child.is_slot = False
    parent_space = Mock()
    parent_space.is_conceptual_space = True
    parent_space.is_basic_level = True
    parent_space.proximity_between.return_value = child_proximity
    root.parent_spaces = [parent_space]
    assert child_proximity == classifier.classify_chunk(root=root, child=child)
