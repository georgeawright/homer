import pytest
from unittest.mock import Mock

from homer.classifiers import SamenessClassifier


def test_same_concepts_classified_as_same():
    common_concept = Mock()
    common_concept.compatibility_with.return_value = 1
    start = Mock()
    start.parent_concept = common_concept
    end = Mock()
    end.parent_concept = common_concept
    classifier = SamenessClassifier()
    start.quality = 1
    end.quality = 1
    assert 1 == classifier.classify_link(start=start, end=end)
    start.quality = 0
    assert 0.5 == classifier.classify_link(start=start, end=end)
    end.quality = 0
    assert 0 == classifier.classify_link(start=start, end=end)


def test_compatible_concepts_classified_as_same():
    start_concept = Mock()
    start_concept.compatibility_with.return_value = 1
    start = Mock()
    start.parent_concept = start_concept
    end_concept = Mock()
    end = Mock()
    end.parent_concept = None
    end.parent_space.parent_concept = end_concept
    classifier = SamenessClassifier()
    start.quality = 1
    end.quality = 1
    assert 1 == classifier.classify_link(start=start, end=end)
    start.quality = 0
    assert 0.5 == classifier.classify_link(start=start, end=end)
    end.quality = 0
    assert 0 == classifier.classify_link(start=start, end=end)


def test_incompatible_concepts_not_classified_as_same():
    start_concept = Mock()
    start = Mock()
    start.parent_concept = start_concept
    end_concept = Mock()
    end = Mock()
    end.parent_concept = end_concept
    start_concept.compatibility_with.return_value = 0
    classifier = SamenessClassifier()
    start.quality = 1
    end.quality = 1
    assert 0 == classifier.classify_link(start=start, end=end)


def test_sameness_of_chunk_no_root():
    classifier = SamenessClassifier()
    assert 1.0 == classifier.classify_chunk(root=None, child=Mock())


def test_sameness_of_chunk_no_child():
    classifier = SamenessClassifier()
    assert 1.0 == classifier.classify_chunk(root=Mock(), child=None)


@pytest.mark.parametrize("proximity", [(0.0), (0.5), (1.0)])
def test_sameness_of_chunk_child_and_root(proximity):
    classifier = SamenessClassifier()
    space = Mock()
    space.is_conceptual_space = True
    space.is_basic_level = True
    space.proximity_between.return_value = proximity
    location = Mock()
    location.space = space
    root = Mock()
    root.locations = [location]
    child = Mock()
    assert proximity == classifier.classify_chunk(root=root, child=child)
