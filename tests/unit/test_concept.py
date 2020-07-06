import math
import pytest

from homer.concept import Concept


@pytest.mark.parametrize(
    "prototype,boundary,distance_metric,candidate,expected",
    [
        ([22], [19], math.dist, [20], 2),
        ([22], [19], math.dist, [21], 1),
        ([22], [19], math.dist, [22], 0),
        ([22], [19], math.dist, [23], 0),
        ([16], None, math.dist, [16], 0),
        ([16], None, math.dist, [10], 6),
        ([16], None, math.dist, [26], 10),
        ([4], [7], math.dist, [7], 3),
        ([4], [7], math.dist, [-20], 0),
        ("hot", None, lambda a, b: 0 if a == b else math.inf, "hot", 0),
        ("cold", None, lambda a, b: 0 if a == b else math.inf, "hot", math.inf),
    ],
)
def test_distance_from(prototype, boundary, distance_metric, candidate, expected):
    concept = Concept(
        "hot", prototype=prototype, boundary=boundary, distance_metric=distance_metric
    )
    assert expected == concept.distance_from(candidate)
