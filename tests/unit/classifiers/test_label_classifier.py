import math
import pytest
from unittest.mock import Mock, patch

from homer.bubbles import Concept, Perceptlet
from homer.classifiers import LabelClassifier
from homer.perceptlet_collection import PerceptletCollection

FLOAT_COMPARISON_TOLERANCE = 1e-1


@pytest.mark.parametrize(
    "proximity_to_prototype, proportion_of_neighbours, expected",
    [
        (0.0, 1.0, 0.4),
        (1.0, 1.0, 1.0),
        (0.0, 0.0, 0.0),
        (0.5, 0.5, 0.5),
        (1.0, 0.0, 0.6),
    ],
)
def test_calculate_confidence(
    proximity_to_prototype,
    proportion_of_neighbours,
    expected,
):
    with patch.object(
        Concept, "proximity_to", return_value=proximity_to_prototype
    ), patch.object(
        PerceptletCollection,
        "proportion_with_label",
        return_value=proportion_of_neighbours,
    ), patch.object(
        Perceptlet, "get_value", return_value=Mock()
    ):
        target_perceptlet = Perceptlet(
            Mock(), [0, 0, 0], Mock(), PerceptletCollection(), Mock()
        )
        concept = Concept("concept_name", Mock())
        classifier = LabelClassifier()
        confidence = classifier.confidence(target_perceptlet, concept)
    assert math.isclose(expected, confidence, abs_tol=FLOAT_COMPARISON_TOLERANCE)
