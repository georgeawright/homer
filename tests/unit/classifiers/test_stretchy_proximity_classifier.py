import pytest
from unittest.mock import Mock

from homer.classifiers import StretchyProximityClassifier


@pytest.mark.parametrize(
    "proximity_weight, neighbours_weight, "
    + "proximity, example_has_neighbours, proportion_of_neighbours, expected",
    [
        (0.5, 0.5, 1.0, True, 1.0, 1.0),
        (0.5, 0.5, 1.0, True, 0.0, 0.5),
        (0.5, 0.5, 0.0, True, 1.0, 0.5),
        (0.6, 0.4, 1.0, True, 1.0, 1.0),
        (0.6, 0.4, 1.0, True, 0.0, 0.6),
        (0.6, 0.4, 0.0, True, 1.0, 0.4),
        (0.6, 0.4, 1.0, False, 0.0, 1.0),
        (0.6, 0.4, 0.0, False, 0.0, 0.0),
    ],
)
def test_classify(
    proximity_weight,
    neighbours_weight,
    proximity,
    example_has_neighbours,
    proportion_of_neighbours,
    expected,
):
    classifier = StretchyProximityClassifier(
        proximity_weight=proximity_weight, neighbours_weight=neighbours_weight
    )
    concept = Mock()
    concept.proximity_to.return_value = proximity
    example = Mock()
    example.has_neighbours.return_value = example_has_neighbours
    example.nearby.proportion_with_label.return_value = proportion_of_neighbours
    assert expected == classifier.classify(concept, example)
