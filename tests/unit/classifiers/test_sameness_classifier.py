import pytest
from unittest.mock import Mock

from homer.classifiers import SamenessClassifier


@pytest.mark.skip
def test_same_concepts_classified_as_same():
    common_concept = Mock()
    start = Mock()
    start.parent_concept = common_concept
    end = Mock()
    end.parent_concept = common_concept
    classifier = SamenessClassifier()
    start.quality = 1
    end.quality = 1
    assert 1 == classifier.classify(start=start, end=end)
    start.quality = 0
    assert 0.5 == classifier.classify(start=start, end=end)
    end.quality = 0
    assert 0 == classifier.classify(start=start, end=end)


@pytest.mark.skip
def test_compatible_concepts_classified_as_same():
    start_concept = Mock()
    start = Mock()
    start.parent_concept = Mock()
    end_concept = Mock()
    end = Mock()
    end.parent_concept = None
    end.parent_space.parent_concept = end_concept
    start_concept.is_compatible_with.return_value = True
    classifier = SamenessClassifier()
    start.quality = 1
    end.quality = 1
    assert 1 == classifier.classify(start=start, end=end)
    start.quality = 0
    assert 0.5 == classifier.classify(start=start, end=end)
    end.quality = 0
    assert 0 == classifier.classify(start=start, end=end)


@pytest.mark.skip
def test_incompatible_concepts_not_classified_as_same():
    start_concept = Mock()
    start = Mock()
    start.parent_concept = start_concept
    end_concept = Mock()
    end = Mock()
    end.parent_concept = end_concept
    start_concept.is_compatible_with.return_value = False
    classifier = SamenessClassifier()
    start.quality = 1
    end.quality = 1
    assert 0 == classifier.classify(start=start, end=end)
