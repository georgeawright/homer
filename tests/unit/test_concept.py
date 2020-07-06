import math
import pytest

from homer.concept import Concept


@pytest.mark.parametrize(
    "depth,boundary,prototype,exception_message",
    [
        (0, None, None, "depth 0 is less than 1."),
        (1, [1], "hot", "a concept with a symbolic prototype cannot have a boundary."),
        (1, [1, 2], [2, 2], "boundary [1, 2] is multidimensional."),
        (1, [1], [2, 2], "have different dimensionality."),
        (1, [1], [1], "prototype and boundary are equal [1]."),
    ],
)
def test_concept_constructor_exceptions(depth, boundary, prototype, exception_message):
    with pytest.raises(Exception) as excinfo:
        Concept("hot", depth=depth, prototype=prototype, boundary=boundary)
    assert exception_message in str(excinfo.value)


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


def test_distance_from_raises_exception_if_no_distance_metric():
    concept = Concept("hot")
    with pytest.raises(Exception) as excinfo:
        concept.distance_from([1])
    assert "Concept hot has no distance metric." in str(excinfo.value)
