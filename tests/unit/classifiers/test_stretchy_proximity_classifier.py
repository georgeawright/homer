import pytest
from unittest.mock import Mock

from homer.classifiers import StretchyProximityClassifier
from homer.structure_collection import StructureCollection


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
    neighbours = StructureCollection()
    if example_has_neighbours:
        neighbour = Mock()
        neighbours.add(neighbour)
        if proportion_of_neighbours == 1:
            neighbour.has_label.return_value = True
        else:
            neighbour.has_label.return_value = False
    example.nearby.return_value = neighbours
    assert expected == classifier.classify(concept, example)
